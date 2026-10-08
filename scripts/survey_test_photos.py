#!/usr/bin/env python3
"""Survey public-domain archives for a 20-photo family-scene test set.

Standard library only. Run from the repository root:

    python scripts/survey_test_photos.py

It (1) counts candidates per source and per route, (2) picks 20 photos from the
Library of Congress FSA/OWI collections by fixed slot rules, checking every
item's own rights statement and downloading each image to verify it and record
its sha256, and (3) writes docs/test-photo-set-survey.md plus the pinned
docs/test-photo-set/selection.json that docs/fetch_test_photos.py downloads.

Anything that could not be done is listed under "Run notes" at the top of the
document; one failing source never fails the run.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import fetch_test_photos as ftp  # noqa: E402

DOC_PATH = os.path.join(ROOT, "docs", "test-photo-set-survey.md")
SELECTION_PATH = ftp.SELECTION_PATH

LOC = "https://www.loc.gov"
COLLECTIONS = {
    "color": "fsa-owi-color-photographs",
    "bw": "fsa-owi-black-and-white-negatives",
}
LOC_INTERVAL = 3.2          # loc.gov JSON API allows 20 requests/minute; blocks for 1 hour beyond it
LOC_CALL_BUDGET = 110
RUN_DEADLINE_S = 14 * 60    # stop picking new photos after this long
MIN_LONG_SIDE = 800
ATTEMPTS_PER_SLOT = 3
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
SMITHSONIAN_API = "https://api.si.edu/openaccess/api/v1.0"
RIGHTS_OK = re.compile(r"no known restrictions|public domain|no known copyright|no copyright restrictions", re.I)
RIGHTS_BAD = re.compile(r"all rights reserved|copyright(ed)? (by|protected)|permission (is )?required", re.I)

# id, subject, lighting, framing, collection, queries tried in order, caption words (any must match title)
SLOTS = [
    ("child-01", "single child", "bright", "close-up", "color", ["girl"], ["girl"]),
    ("child-02", "single child", "bright", "medium", "color", ["boy"], ["boy"]),
    ("child-03", "single child", "indoor", "close-up", "color", ["baby"], ["baby", "infant"]),
    ("child-04", "single child", "backlit", "medium", "color", ["child sunset", "boy sunset"], ["child", "boy", "girl"]),
    ("child-05", "single child", "indoor", "medium", "bw", ["girl kitchen", "girl school"], ["girl"]),
    ("group-01", "group", "bright", "wide", "color", ["children playing"], ["children", "kids", "boys", "girls"]),
    ("group-02", "group", "indoor", "medium", "bw", ["children school"], ["children", "pupils", "students"]),
    ("group-03", "group", "bright", "wide", "color", ["boys swimming", "children swimming"], ["boys", "children", "girls"]),
    ("group-04", "group", "low light", "wide", "bw", ["children night"], ["children", "boys", "girls"]),
    ("family-01", "adults with children", "bright", "medium", "color", ["family"], ["family"]),
    ("family-02", "adults with children", "indoor", "medium", "color", ["mother children"], ["mother"]),
    ("family-03", "adults with children", "bright", "medium", "bw", ["father son", "father children"], ["father"]),
    ("family-04", "adults with children", "indoor", "wide", "bw", ["family dinner", "family table"], ["family"]),
    ("family-05", "adults with children", "backlit", "wide", "color", ["family sunset", "family porch"], ["family"]),
    ("pet-01", "pets", "bright", "medium", "color", ["dog"], ["dog"]),
    ("pet-02", "pets", "indoor", "close-up", "bw", ["cat"], ["cat", "kitten"]),
    ("pet-03", "pets", "bright", "close-up", "bw", ["puppy"], ["puppy", "puppies", "dog"]),
    ("object-01", "objects", "indoor", "close-up", "bw", ["doll", "toys"], ["doll", "toy"]),
    ("object-02", "objects", "indoor", "medium", "color", ["kitchen"], ["kitchen"]),
    ("object-03", "objects", "low light", "medium", "color", ["christmas tree"], ["christmas", "tree"]),
]
# Used only when a slot above finds nothing usable, to keep the set at 20.
RESERVE = [
    ("extra-01", "adults with children", "bright", "wide", "color", ["farm family"], ["family"]),
    ("extra-02", "group", "bright", "medium", "color", ["children"], ["children"]),
    ("extra-03", "single child", "bright", "wide", "bw", ["boy farm", "boy yard"], ["boy"]),
    ("extra-04", "adults with children", "indoor", "medium", "bw", ["mother baby"], ["mother", "baby"]),
    ("extra-05", "pets", "bright", "wide", "color", ["dog children"], ["dog"]),
    ("extra-06", "objects", "bright", "wide", "color", ["house yard"], ["house", "yard"]),
]
SUBJECTS = ["single child", "group", "adults with children", "pets", "objects"]
LIGHTING = ["bright", "indoor", "low light", "backlit"]
FRAMING = ["close-up", "medium", "wide"]

NOTES = []   # run notes: what was skipped or fell back


def note(message):
    NOTES.append(message)
    print("NOTE: " + message, flush=True)


def log(message):
    print(message, flush=True)


def sha1_key(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()


class LocClient:
    """Rate-limited loc.gov JSON client (20 requests/minute documented limit)."""

    def __init__(self):
        self.calls = 0
        self.last = 0.0
        self.blocked = False
        self.cache = {}

    def get_json(self, url):
        if url in self.cache:
            return self.cache[url]
        if self.blocked:
            raise RuntimeError("loc.gov JSON API stopped for this run after repeated throttling")
        if self.calls >= LOC_CALL_BUDGET:
            raise RuntimeError("loc.gov call budget (%d) used up" % LOC_CALL_BUDGET)
        wait = LOC_INTERVAL - (time.time() - self.last)
        if wait > 0:
            time.sleep(wait)
        self.calls += 1
        try:
            raw = ftp.http_get(url, retries=3, pause=5.0, accept="application/json", log=log)
        except RuntimeError as err:
            if "429" in str(err):
                self.blocked = True
            self.last = time.time()
            raise
        self.last = time.time()
        try:
            data = json.loads(raw.decode("utf-8"))
        except ValueError:
            raise RuntimeError("non-JSON answer (CAPTCHA or error page?) from %s" % url)
        self.cache[url] = data
        return data

    def collection_url(self, key, query=None, per_page=1, extra=""):
        url = "%s/collections/%s/?fo=json&at=results,pagination&c=%d" % (LOC, COLLECTIONS[key], per_page)
        if query:
            url += "&q=" + urllib.parse.quote_plus(query)
        return url + extra

    def count(self, url):
        data = self.get_json(url)
        pagination = data.get("pagination") or {}
        if isinstance(pagination.get("of"), int):
            return pagination["of"]
        if isinstance(pagination.get("total"), int) and pagination.get("perpage") == 1:
            return pagination["total"]
        raise RuntimeError("no pagination.of in answer from %s" % url)


def survey_loc(loc):
    """Counts per route for the two FSA/OWI collections and the site-wide photo format."""
    rows = []

    def add(route, label, url):
        try:
            rows.append({"source": "Library of Congress", "route": route, "query": label, "count": loc.count(url), "error": None})
        except RuntimeError as err:
            rows.append({"source": "Library of Congress", "route": route, "query": label, "count": None, "error": str(err)})
            note("LoC route '%s' (%s) failed: %s" % (route, label, err))

    for key in ("color", "bw"):
        add("collection endpoint /collections/%s/" % COLLECTIONS[key], "(all items)", loc.collection_url(key))
    for query in ("family", "children", "dog"):
        for key in ("color", "bw"):
            add("collection endpoint /collections/%s/" % COLLECTIONS[key], "q=" + query, loc.collection_url(key, query))
        add("site-wide photo format /photos/", "q=" + query,
            "%s/photos/?fo=json&at=results,pagination&c=1&q=%s" % (LOC, urllib.parse.quote_plus(query)))
    return rows


def check_plausible(rows):
    """Flag a failed read: zero or tiny counts where thousands are expected."""
    totals = [r for r in rows if r["query"] == "(all items)"]
    ok = [r for r in totals if r["count"] is not None]
    if not ok:
        return "LoC collection totals could not be read at all"
    bad = [r for r in ok if r["count"] < 100]
    if bad:
        return "LoC collection totals implausibly small (%s)" % ", ".join(str(r["count"]) for r in bad)
    return None


# ---------------------------------------------------------------- selection

def https(url):
    if url.startswith("//"):
        url = "https:" + url
    return re.sub(r"^http://", "https://", url)


def item_url_of(result):
    url = result.get("url") or result.get("id") or ""
    url = https(url).split("?")[0]
    if "/item/" not in url:
        return None
    return url if url.endswith("/") else url + "/"


def item_id_of(item_url):
    return item_url.rstrip("/").rsplit("/", 1)[-1]


def walk(node, key=""):
    """Yield (key, value) for every scalar in a JSON structure."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, str(k))
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, key)
    else:
        yield key, node


def rights_statements(item_json):
    found = []
    for key, value in walk(item_json.get("item") or {}):
        if "rights" in key.lower() and isinstance(value, str) and value.strip():
            text = re.sub(r"<[^>]+>", " ", value)
            text = re.sub(r"\s+", " ", text).strip()
            if text not in found:
                found.append(text)
    return found


def rights_ok(statements):
    joined = " ".join(statements)
    return bool(RIGHTS_OK.search(joined)) and not RIGHTS_BAD.search(joined)


def jpeg_candidates(item_json, result):
    """Image URLs for the item, best first: JPEGs from resource files by width, then listed image_url."""
    sized = []
    for node in walk_dicts(item_json.get("resources") or []):
        url = node.get("url")
        if not isinstance(url, str):
            continue
        mimetype = str(node.get("mimetype", ""))
        if mimetype == "image/jpeg" or re.search(r"\.jpe?g$", url, re.I):
            sized.append((int(node.get("width") or 0), int(node.get("size") or 0), https(url)))
    sized.sort(reverse=True)
    urls = [u for _, _, u in sized]
    listed = [https(u) for u in (result.get("image_url") or []) if re.search(r"\.jpe?g$", u, re.I)]
    for url in reversed(listed):
        if url not in urls:
            urls.append(url)
    return urls


def walk_dicts(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk_dicts(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_dicts(v)


def creator_of(item_json, result):
    names = []
    item = item_json.get("item") or {}
    for source in (item.get("contributor_names"), item.get("contributors"), result.get("contributor")):
        if isinstance(source, list):
            for entry in source:
                if isinstance(entry, dict):
                    names.extend(str(k) for k in entry)
                elif isinstance(entry, str):
                    names.append(entry)
    for name in names:
        if "photographer" in name.lower():
            parts = [p.strip() for p in re.sub(r",?\s*photographer\.?$", "", name.strip(), flags=re.I).split(",")]
            parts = [p for p in parts if p]
            return " ".join(reversed(parts[:2])).title() if parts else name
    return "Unknown photographer (FSA/OWI)"


def first_text(item, *keys):
    for key in keys:
        value = item.get(key)
        if isinstance(value, list) and value:
            value = value[0]
        if isinstance(value, str) and value.strip():
            return re.sub(r"\s+", " ", value).strip()
    return ""


def pick_for_slot(loc, slot, taken, as_of, deadline):
    """Return a selection record for the slot, or None, trying candidates in hash order."""
    slot_id, subject, lighting, framing, collection, queries, words = slot
    word_re = re.compile(r"\b(%s)\b" % "|".join(re.escape(w) for w in words), re.I)
    attempts = 0
    for query in queries:
        try:
            data = loc.get_json(loc.collection_url(collection, query, per_page=100))
        except RuntimeError as err:
            note("slot %s: search '%s' failed: %s" % (slot_id, query, err))
            continue
        results = [r for r in data.get("results") or [] if isinstance(r, dict)]
        cands = []
        for result in results:
            url = item_url_of(result)
            title = str(result.get("title") or "")
            if url and url not in taken and word_re.search(title):
                cands.append((sha1_key(slot_id, url), url, result))
        log("slot %s q=%r: %d results, %d caption matches" % (slot_id, query, len(results), len(cands)))
        for _, url, result in sorted(cands):
            if attempts >= ATTEMPTS_PER_SLOT or time.time() > deadline:
                return None
            attempts += 1
            record = try_item(loc, slot, query, url, result, as_of)
            if record:
                return record
    return None


def try_item(loc, slot, query, url, result, as_of):
    slot_id, subject, lighting, framing, collection, _, _ = slot
    try:
        item_json = loc.get_json(url + "?fo=json&at=item,resources")
    except RuntimeError as err:
        note("slot %s: item %s unreadable: %s" % (slot_id, url, err))
        return None
    statements = rights_statements(item_json)
    if not rights_ok(statements):
        log("  reject %s: rights statement not clearly public domain: %r" % (url, statements[:2]))
        return None
    item = item_json.get("item") or {}
    for image_url in jpeg_candidates(item_json, result)[:3]:
        try:
            data = ftp.http_get(image_url, log=log)
        except RuntimeError as err:
            log("  image %s unreadable: %s" % (image_url, err))
            continue
        size = ftp.jpeg_size(data)
        if not size or max(size) < MIN_LONG_SIDE:
            log("  image %s too small or not a JPEG (%s)" % (image_url, size))
            continue
        creator = creator_of(item_json, result)
        title = first_text(item, "title") or str(result.get("title") or "")
        date = first_text(item, "date", "created_published") or str(result.get("date") or "")
        rights = " | ".join(statements)[:400]
        return {
            "slot": slot_id, "id": "loc:" + item_id_of(url), "item_url": url, "image_url": image_url,
            "creator": creator, "title": title, "date": date,
            "license": "Public domain (LoC rights statement: %s)" % rights,
            "rights_text": rights, "rights_url": url, "rights_checked_at": as_of,
            "attribution": "%s, \"%s\"%s, Library of Congress Prints & Photographs Division, FSA/OWI Collection, %s."
                           % (creator, title.rstrip("."), " (%s)" % date if date else "", url),
            "subject": subject, "lighting": lighting, "framing": framing,
            "tone": "color (Kodachrome scan)" if collection == "color" else "black-and-white (negative scan)",
            "collection": COLLECTIONS[collection], "query": query,
            "width": size[0], "height": size[1], "bytes": len(data), "sha256": ftp.sha256_bytes(data),
        }
    log("  no usable JPEG for %s" % url)
    return None


def select_photos(loc, as_of):
    start = time.time()
    deadline = start + RUN_DEADLINE_S
    chosen, taken, unfilled = [], set(), []
    for slot in SLOTS:
        record = pick_for_slot(loc, slot, taken, as_of, deadline)
        if record:
            chosen.append(record)
            taken.add(record["item_url"])
            log("  -> %s %s" % (slot[0], record["item_url"]))
        else:
            unfilled.append(slot)
            note("slot %s (%s, %s, %s) found nothing usable" % (slot[0], slot[1], slot[2], slot[3]))
    for slot in RESERVE:
        if len(chosen) >= len(SLOTS):
            break
        record = pick_for_slot(loc, slot, taken, as_of, deadline)
        if record:
            chosen.append(record)
            taken.add(record["item_url"])
            note("reserve slot %s (%s) used to replace an unfilled slot" % (slot[0], slot[1]))
    return chosen, unfilled


# ---------------------------------------------------------------- other sources

def api_json(url):
    raw = ftp.http_get(url, retries=3, pause=4.0, accept="application/json", log=log)
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError:
        raise RuntimeError("non-JSON answer from %s" % url)


def survey_commons():
    """Wikimedia Commons: search count, category counts, and a per-file licence histogram."""
    rows, histogram = [], {}
    source = "Wikimedia Commons"

    def add(route, label, fn):
        try:
            rows.append({"source": source, "route": route, "query": label, "count": fn(), "error": None})
        except (RuntimeError, KeyError, TypeError) as err:
            rows.append({"source": source, "route": route, "query": label, "count": None, "error": str(err)})
            note("Commons route '%s' (%s) failed: %s" % (route, label, err))

    for query in ("family photograph", "children playing"):
        url = "%s?action=query&format=json&list=search&srnamespace=6&srlimit=1&srinfo=totalhits&srsearch=%s" % (
            COMMONS_API, urllib.parse.quote_plus(query + " filetype:bitmap"))
        add("MediaWiki search list=search (File: namespace)", "q=" + query,
            lambda url=url: api_json(url)["query"]["searchinfo"]["totalhits"])
    cats = ["Category:Family photographs", "Category:Photographs of children",
            "Category:Farm Security Administration photographs", "Category:Children playing"]
    try:
        data = api_json("%s?action=query&format=json&prop=categoryinfo&titles=%s" % (
            COMMONS_API, urllib.parse.quote("|".join(cats))))
        for page in (data.get("query", {}).get("pages") or {}).values():
            files = (page.get("categoryinfo") or {}).get("files")
            missing = "missing" in page
            rows.append({"source": source, "route": "category info (prop=categoryinfo)", "query": page.get("title", "?"),
                         "count": None if missing else files,
                         "error": "category does not exist" if missing else None})
    except RuntimeError as err:
        note("Commons category route failed: %s" % err)
        rows.append({"source": source, "route": "category info (prop=categoryinfo)", "query": "; ".join(cats), "count": None, "error": str(err)})
    try:
        url = ("%s?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=50&gsrsearch=%s"
               "&prop=imageinfo&iiprop=extmetadata&iiextmetadatafilter=LicenseShortName"
               % (COMMONS_API, urllib.parse.quote_plus("family photograph filetype:bitmap")))
        for page in (api_json(url).get("query", {}).get("pages") or {}).values():
            info = (page.get("imageinfo") or [{}])[0]
            lic = (info.get("extmetadata") or {}).get("LicenseShortName", {}).get("value", "(none stated)")
            histogram[lic] = histogram.get(lic, 0) + 1
    except RuntimeError as err:
        note("Commons licence-histogram route failed: %s" % err)
    return rows, histogram


def survey_smithsonian():
    """Smithsonian Open Access: counts for two queries, and the per-item media usage values of one page."""
    key = os.environ.get("SMITHSONIAN_API_KEY") or "DEMO_KEY"
    rows, histogram = [], {}
    source = "Smithsonian Open Access"
    queries = [("family photograph", 'family photograph AND online_media_type:"Images"'),
               ("children", 'children AND online_media_type:"Images"')]
    for label, q in queries:
        url = "%s/search?rows=50&api_key=%s&q=%s" % (SMITHSONIAN_API, urllib.parse.quote(key), urllib.parse.quote_plus(q))
        try:
            data = api_json(url)
            rows.append({"source": source, "route": "api.si.edu /search (rowCount)", "query": "q=" + label,
                         "count": data["response"]["rowCount"], "error": None})
            if not histogram:
                for node in walk_dicts(data["response"].get("rows") or []):
                    if "access" in node and isinstance(node["access"], str):
                        histogram[node["access"]] = histogram.get(node["access"], 0) + 1
        except (RuntimeError, KeyError, TypeError) as err:
            rows.append({"source": source, "route": "api.si.edu /search (rowCount)", "query": "q=" + label,
                         "count": None, "error": str(err)})
            note("Smithsonian route (%s) failed: %s" % (label, err))
        time.sleep(1.0)
    if key == "DEMO_KEY":
        note("SMITHSONIAN_API_KEY not set; the Smithsonian counts used the shared DEMO_KEY, which is heavily rate limited")
    return rows, histogram


# ---------------------------------------------------------------- document

def tally(photos, field, order):
    return [(value, sum(1 for p in photos if p[field] == value)) for value in order]


def count_text(row):
    return "%s" % row["count"] if row["count"] is not None else "FAILED (%s)" % (row["error"] or "no answer")


def render(as_of, rows, photos, unfilled, histograms, failed_read, loc_calls):
    out = ["# Test photo set survey: public-domain archives", ""]
    out.append("As-of date of the fetch: %s (UTC). Generated by `scripts/survey_test_photos.py`; do not edit by hand." % as_of)
    out.append("")
    if failed_read:
        out.append("**FAILED READ:** %s. Counts below are not what the source holds; rerun before relying on them." % failed_read)
        out.append("")
    out.append("## Run notes")
    out.append("")
    out.extend(["- " + n for n in NOTES] or ["- No fallbacks, skips or failed routes in this run."])
    out.append("")
    out.append("## What was read")
    out.append("")
    out.append("Sources visited: Library of Congress (loc.gov JSON API, FSA/OWI collections), Wikimedia Commons (MediaWiki API), "
               "Smithsonian Open Access (api.si.edu). Selection was made from the Library of Congress only; "
               "the other two were counted and sampled to judge them as candidates. "
               "loc.gov API calls made: %d (documented limit 20 requests/minute, so calls are spaced %.1fs apart)." % (loc_calls, LOC_INTERVAL))
    out.append("")
    out.append("| Source | Route | Query | Count |")
    out.append("|---|---|---|---|")
    for r in rows:
        out.append("| %s | %s | %s | %s |" % (r["source"], r["route"], r["query"], count_text(r)))
    out.append("")
    out.append("Counts for the same query by different routes legitimately differ (a collection endpoint is a subset of the site-wide "
               "format endpoint, and Commons search counts are full-text hits, not licence-checked photos); a count of zero is treated as a failed read.")
    for name, hist in histograms.items():
        out.append("")
        out.append("Per-item rights values seen in a 50-item sample, %s: %s." % (
            name, ", ".join("%s x%d" % kv for kv in sorted(hist.items(), key=lambda kv: -kv[1])) or "none read"))
    out.append("")
    out.append("## Candidate sources")
    out.append("")
    out.append("| Source | Licence / rights | Commit and reuse clearly allowed? | Attribution | Scriptable fetch | Rights unclear? |")
    out.append("|---|---|---|---|---|---|")
    out.append("| Library of Congress, FSA/OWI color and black-and-white collections | Per-item rights advisory; most FSA/OWI items say no known restrictions on publication (US federal photographers, pre-1950) | Yes where the item's own statement says so; this script records and checks it per item | Not required; credit is requested (photographer, LoC P&P Division, item URL) | Yes: JSON API, 20 requests/minute, no key | Collection-level default is not trusted; any item without a matching statement is rejected |")
    out.append("| Wikimedia Commons | Per-file licence from extmetadata (public domain, CC0, CC BY, CC BY-SA and others mixed in the same search) | Only for files whose own licence is public domain or CC0; CC BY(-SA) adds attribution and share-alike duties | Required for CC BY/BY-SA | Yes: MediaWiki API, no key | Yes: mixed licences and per-file uploader claims; verify each file page and check the depicted-person rights |")
    out.append("| Smithsonian Open Access | CC0 on items flagged CC0 in media usage; other items restricted | Only items whose own usage field says CC0 | Not required; credit requested | Yes: api.si.edu needs a free key (DEMO_KEY is heavily limited) | Yes: collection is mixed, not all online images are CC0 |")
    out.append("")
    out.append("Not examined by this variation: open-license photo sites, team-shot options, NARA catalog (needs a key), Europeana, Flickr Commons.")
    out.append("")
    out.append("## Recommended set")
    out.append("")
    if len(photos) != ftp.EXPECTED_COUNT:
        out.append("**INCOMPLETE:** %d of %d photos were selected; see Run notes. The fetch script refuses an incomplete selection."
                   % (len(photos), ftp.EXPECTED_COUNT))
        out.append("")
    out.append("Selection rule: per slot, search the LoC collection, keep results whose caption has a slot keyword, order by sha1(slot id + item URL) "
               "(neither alphabetical nor newest-first), then take the first whose own rights statement matches a public-domain pattern and whose JPEG is at least %d px on the long side. "
               "Subject, lighting and framing are assigned by slot intent plus caption keywords and are not visually verified." % MIN_LONG_SIDE)
    out.append("")
    out.append("| # | Slot | ID / URL | Creator | License (rights statement as recorded) | Attribution string | Subject | Lighting | Framing | Tone | Resolution |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, p in enumerate(photos, 1):
        cells = [str(i), p["slot"], "%s (%s)" % (p["id"], p["item_url"]), p["creator"], p["license"], p["attribution"],
                 p["subject"], p["lighting"], p["framing"], p["tone"], "%dx%d" % (p["width"], p["height"])]
        out.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    out.append("")
    out.append("Pinned selection (read by `docs/fetch_test_photos.py` if `docs/test-photo-set/selection.json` is absent), with sha256 per image:")
    out.append("")
    out.append("```json selection")
    out.append(json.dumps({"as_of": as_of, "complete": len(photos) == ftp.EXPECTED_COUNT, "photos": photos}, indent=1, ensure_ascii=False))
    out.append("```")
    out.append("")
    out.append("## Coverage mix")
    out.append("")
    for title, field, order in (("Subjects", "subject", SUBJECTS), ("Lighting", "lighting", LIGHTING), ("Framing", "framing", FRAMING)):
        out.append("- %s: %s" % (title, ", ".join("%s %d" % kv for kv in tally(photos, field, order))))
    tones = {}
    for p in photos:
        tones[p["tone"]] = tones.get(p["tone"], 0) + 1
    out.append("- Tone: %s" % ", ".join("%s %d" % kv for kv in sorted(tones.items())))
    out.append("")
    out.append("Gaps and reasons:")
    for slot in unfilled:
        out.append("- Slot %s (%s, %s, %s) was not filled by its own queries: no candidate passed the caption, rights and resolution checks in %d tries." % (
            slot[0], slot[1], slot[2], slot[3], ATTEMPTS_PER_SLOT))
    for title, field, order, want in (("subject", "subject", SUBJECTS, 3), ("lighting", "lighting", LIGHTING, 2), ("framing", "framing", FRAMING, 5)):
        for value, n in tally(photos, field, order):
            if n < want:
                out.append("- Fewer than %d %s photos labelled '%s' (%d): the mid-century documentary archive has few such scenes that also pass the rights and resolution checks." % (want, title, value, n))
    out.append("- Scanned black-and-white negatives and Kodachrome scans are a tradeoff for coloring comparisons: the black-and-white items have no colour ground truth, and film grain and scan tone differ from phone snapshots. No modern digital snapshots, no screens or phone-camera noise.")
    out.append("- No photo here has been looked at by a person or a vision model; lighting and framing labels are intent, not measurement.")
    out.append("")
    out.append("## Rights risks")
    out.append("")
    out.append("- Public-domain copyright status does not settle privacy or personality rights. These are documentary photographs of identifiable children and adults taken without model releases; no release exists or can be obtained.")
    out.append("- Most subjects were photographed 80 or more years ago, but a few may be alive; do not publish names from captions next to faces, and do not use the images in ways that imply endorsement or a sensitive claim about the person.")
    out.append("- The rights statement is a statement by the holding institution (no known restrictions), not a guarantee; it is recorded per item with its URL and the as-of date so it can be re-checked.")
    out.append("- Avoid: items whose statement mentions restrictions or permission, items from the same collection without their own statement, Commons files with CC BY-SA or unclear uploader claims, and any modern photo of an identifiable child without a signed release.")
    out.append("")
    out.append("## Fetch script")
    out.append("")
    out.append("`docs/fetch_test_photos.py` (standard library only) downloads exactly the 20 listed photos from their stable image URLs into `--out` (default `test-photos/`) and writes `ATTRIBUTION.md` there. "
               "Run: `python docs/fetch_test_photos.py --out test-photos`; check existing files with `--verify-only`. "
               "It verifies the JPEG signature and the pinned sha256 for each file, retries network errors and HTTP 429/5xx with backoff, writes through a `.part` file, "
               "skips files that already verify (idempotent reruns), attempts every photo even after a failure, and exits 1 if any photo fails or the selection is not exactly 20 distinct photos. "
               "Not done: it cannot detect a photo that was replaced by the source with another valid JPEG unless the sha256 differs, which it reports as a failure.")
    out.append("")
    out.append("## Open questions")
    out.append("")
    out.append("- Round 1 (acceptance): is a LoC-only set acceptable, or must some photos be modern colour digital snapshots from a source with releases?")
    out.append("- Round 1 (labels): should lighting, framing and subject labels be confirmed by a person or vision model before the set is committed?")
    out.append("- Round 2 (resolution): is %d px on the long side enough for the coloring comparison, or are the full-size TIFF masters needed?" % MIN_LONG_SIDE)
    out.append("- Round 2 (tone): are black-and-white scans wanted as inputs, or only colour originals?")
    out.append("- Round 3 (sources): should Smithsonian (with a real key), NARA and Europeana be searched with the same per-item rights checks?")
    out.append("")
    return "\n".join(out)


def main():
    as_of = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    loc = LocClient()
    rows = []
    try:
        rows.extend(survey_loc(loc))
    except Exception as err:  # keep going: a broken source must not end the run
        note("LoC counting stopped: %s" % err)
    commons_rows, commons_hist = survey_commons()
    si_rows, si_hist = survey_smithsonian()
    rows.extend(commons_rows + si_rows)
    failed_read = check_plausible(rows)
    if failed_read:
        note("FAILED READ: " + failed_read)

    photos, unfilled = select_photos(loc, as_of)
    histograms = {}
    if commons_hist:
        histograms["Wikimedia Commons (LicenseShortName)"] = commons_hist
    if si_hist:
        histograms["Smithsonian (media usage access)"] = si_hist
    if len(photos) < ftp.EXPECTED_COUNT:
        note("only %d of %d photos selected" % (len(photos), ftp.EXPECTED_COUNT))

    doc = render(as_of, rows, photos, unfilled, histograms, failed_read, loc.calls)
    os.makedirs(os.path.dirname(SELECTION_PATH), exist_ok=True)
    with open(SELECTION_PATH, "w", encoding="utf-8") as handle:
        json.dump({"as_of": as_of, "complete": len(photos) == ftp.EXPECTED_COUNT, "photos": photos}, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    with open(DOC_PATH, "w", encoding="utf-8") as handle:
        handle.write(doc)
    print()
    print(doc)
    produced = photos or any(r["count"] for r in rows)
    return 0 if produced else 1


if __name__ == "__main__":
    sys.exit(main())
