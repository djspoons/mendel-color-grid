#!/usr/bin/env python3
"""Survey open-license photo APIs and pin a 20-photo family test set.

Queries Openverse (search + stats routes) and Wikimedia Commons (search +
category routes), keeps only CC0 / public-domain JPEGs, fills a fixed
subject x lighting x framing grid one cell at a time, downloads each chosen
photo to record its SHA-256, then writes:

  docs/test-photo-set-manifest.json   the pinned selection (input of the fetch script)
  docs/test-photo-set-survey.md       the findings document

Standard library only. Run from the repository root:

    python scripts/survey_test_photos.py
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import fetch_test_photos as fetcher  # noqa: E402

MANIFEST_PATH = os.path.join(ROOT, "docs", "test-photo-set-manifest.json")
REPORT_PATH = os.path.join(ROOT, "docs", "test-photo-set-survey.md")
REPORT_RELATIVE = "docs/test-photo-set-survey.md"

OPENVERSE = "https://api.openverse.org/v1"
COMMONS = "https://commons.wikimedia.org/w/api.php"
COMMONS_LICENSE_CATEGORIES = ("CC-Zero", "PD-self")
OPENVERSE_LICENSES = "cc0,pdm"

MIN_LONG, MIN_SHORT = 1600, 1000
MAX_COMMONS_BYTES = 10 * 1024 * 1024
MAX_PER_CREATOR = 2
TRIES_PER_CELL = 6
TIME_BUDGET_SECONDS = 12 * 60
PAUSE = 0.4
TITLE_BLOCKLIST = ("drawing", "illustration", "painting", "statue", "logo", "map of",
                   "poster", "stamp", "diagram", "sculpture", "cartoon", "postcard")

SUBJECTS = ("single child", "group", "adults with children", "pets", "objects")
LIGHTING = ("bright", "indoor", "low light", "backlit")
FRAMING = ("close-up", "medium", "wide")

CHILD = ("child", "kid", "boy", "girl", "toddler", "baby", "children", "kids")
GROUP = ("group", "children", "kids", "friends", "family", "party", "team")
ADULTS = ("mother", "father", "parent", "family", "mom", "dad", "grandmother",
          "grandfather", "grandparent", "daughter", "son")
PET = ("dog", "cat", "puppy", "kitten", "pet")

# The fixed coverage grid: filled in this order, one photo per cell.
# (cell id, subject, lighting, framing, search terms, words one of which must
#  appear in the title / tags / description / categories)
GRID = (
    ("c01", "single child", "bright", "close-up", "child portrait smiling", CHILD),
    ("c02", "single child", "bright", "medium", "child playing outdoors", CHILD),
    ("c03", "single child", "bright", "wide", "child playing in park", CHILD),
    ("c04", "single child", "indoor", "close-up", "child portrait indoors", CHILD),
    ("c05", "single child", "indoor", "medium", "child playing at home", CHILD),
    ("c06", "single child", "low light", "medium", "child evening dusk", CHILD),
    ("c07", "single child", "backlit", "medium", "child silhouette sunset", CHILD),
    ("c08", "group", "bright", "medium", "children playing together", GROUP),
    ("c09", "group", "bright", "wide", "family picnic park", GROUP),
    ("c10", "group", "indoor", "medium", "family dinner table", GROUP),
    ("c11", "group", "low light", "wide", "birthday party candles", ("party", "birthday", "candles", "children")),
    ("c12", "adults with children", "bright", "medium", "mother with child outdoors", ADULTS),
    ("c13", "adults with children", "indoor", "close-up", "father holding baby", ADULTS + ("baby",)),
    ("c14", "adults with children", "backlit", "wide", "family sunset beach", ADULTS),
    ("c15", "pets", "bright", "close-up", "dog portrait", PET),
    ("c16", "pets", "bright", "wide", "dog running in park", PET),
    ("c17", "pets", "indoor", "medium", "cat on sofa at home", PET),
    ("c18", "pets", "low light", "close-up", "cat at night", PET),
    ("c19", "objects", "indoor", "close-up", "toys on floor children room", ("toy", "toys", "teddy", "blocks", "doll")),
    ("c20", "objects", "bright", "wide", "backyard garden house", ("garden", "backyard", "house", "home", "playground", "yard")),
)

# Terms used only for the side-by-side candidate counts.
COUNT_TERMS = ("child", "children playing", "family", "dog", "cat", "kitchen", "birthday", "picnic")
COUNT_SOURCES = ("stocksnap", "wikimedia", "flickr")
COMMONS_CATEGORIES = ("CC-Zero", "PD-self")


class Run:
    """Collects what was read and anything that went wrong along the way."""

    def __init__(self):
        self.started = time.time()
        self.as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        self.notes = []
        self.counts = []   # (source, route, query, filter, count or None)
        self.stats = None  # Openverse per-source totals

    def note(self, message):
        print("NOTE: " + message, file=sys.stderr)
        self.notes.append(message)

    def over_budget(self):
        return time.time() - self.started > TIME_BUDGET_SECONDS


def get_json(run, url):
    """GET JSON; on failure record a note and return None."""
    time.sleep(PAUSE)
    try:
        return json.loads(fetcher.http_get(url, max_bytes=5 * 1024 * 1024).decode("utf-8"))
    except (fetcher.FetchError, ValueError) as err:
        run.note("request failed: %s" % err)
        return None


def strip_html(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def jpeg_size(data):
    """(width, height) from the first SOF marker, or None when not a JPEG."""
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0xFF:
            i += 1
        elif marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
        elif 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return (int.from_bytes(data[i + 7:i + 9], "big"),
                    int.from_bytes(data[i + 5:i + 7], "big"))
        else:
            i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
    return None


# --- Openverse ---------------------------------------------------------

def openverse_url(query, page=1, source=None, extension=True):
    params = {"q": query, "license": OPENVERSE_LICENSES, "category": "photograph",
              "mature": "false", "page_size": 20, "page": page}
    if extension:
        params["extension"] = "jpg"
    if source:
        params["source"] = source
    return OPENVERSE + "/images/?" + urllib.parse.urlencode(params)


def openverse_count(run, query, source=None):
    data = get_json(run, openverse_url(query, source=source, extension=False))
    count = data.get("result_count") if data else None
    route = "search API" + (", source=%s" % source if source else "")
    run.counts.append(("Openverse", route, query, "license=cc0,pdm; category=photograph", count))


def openverse_stats(run):
    data = get_json(run, OPENVERSE + "/images/stats/")
    if isinstance(data, list) and data:
        run.stats = sorted(data, key=lambda s: -int(s.get("media_count") or 0))


def openverse_candidates(run, query):
    found = []
    for page in (1, 2):
        data = get_json(run, openverse_url(query, page=page))
        if not data:
            break
        for item in data.get("results", []):
            if item.get("license") not in ("cc0", "pdm"):
                continue
            if not (item.get("width") and item.get("height") and item.get("url")):
                continue
            version = item.get("license_version") or ""
            text = ("CC0 %s Universal" if item["license"] == "cc0" else "Public Domain Mark %s") % version
            found.append({
                "source": "openverse", "id": item["id"], "title": item.get("title") or "untitled",
                "creator": item.get("creator") or "unknown", "license": item["license"],
                "license_version": version, "license_text": text.strip(),
                "license_url": item.get("license_url") or "",
                "landing_url": item.get("foreign_landing_url") or item["url"],
                "url": item["url"], "width": int(item["width"]), "height": int(item["height"]),
                "mime": "image/jpeg", "bytes": None, "api_sha1": None,
                "origin": item.get("source") or "",
                "text": " ".join([item.get("title") or ""] + [t.get("name", "") for t in item.get("tags") or []]).lower(),
            })
    return found


# --- Wikimedia Commons --------------------------------------------------

def commons_url(**params):
    base = {"action": "query", "format": "json", "formatversion": 2}
    base.update(params)
    return COMMONS + "?" + urllib.parse.urlencode(base)


def commons_count(run, query, category):
    url = commons_url(list="search", srnamespace=6, srlimit=1, srinfo="totalhits",
                      srsearch="filetype:bitmap incategory:%s %s" % (category, query))
    data = get_json(run, url)
    hits = data["query"]["searchinfo"]["totalhits"] if data and "query" in data else None
    run.counts.append(("Wikimedia Commons", "search (list=search, incategory:%s)" % category,
                       query, "namespace File, bitmap", hits))


def commons_category_counts(run):
    titles = "|".join("Category:" + c for c in COMMONS_CATEGORIES)
    data = get_json(run, commons_url(titles=titles, prop="categoryinfo"))
    for page in (data or {}).get("query", {}).get("pages", []):
        info = page.get("categoryinfo")
        count = info.get("files") if info else None
        run.counts.append(("Wikimedia Commons", "category listing (categoryinfo)", page.get("title", "?"),
                           "all file types, all subjects", count))


def commons_candidates(run, query):
    found = []
    for category in COMMONS_LICENSE_CATEGORIES:
        url = commons_url(generator="search", gsrnamespace=6, gsrlimit=50, prop="imageinfo",
                          gsrsearch="filetype:bitmap incategory:%s %s" % (category, query),
                          iiprop="url|size|sha1|mime|extmetadata",
                          iiextmetadatafilter="Artist|LicenseShortName|LicenseUrl|ImageDescription|Categories")
        data = get_json(run, url)
        for page in (data or {}).get("query", {}).get("pages", []):
            info = (page.get("imageinfo") or [{}])[0]
            meta = info.get("extmetadata") or {}
            short = strip_html((meta.get("LicenseShortName") or {}).get("value"))
            lowered = short.lower()
            if not (lowered.startswith("cc0") or lowered.startswith("public domain") or lowered.startswith("pd")):
                continue
            if info.get("mime") != "image/jpeg" or not info.get("url"):
                continue
            if int(info.get("size") or 0) > MAX_COMMONS_BYTES:
                continue
            title = page.get("title", "")
            filename = title.split(":", 1)[-1]
            found.append({
                "source": "commons", "id": str(page.get("pageid")), "title": filename,
                "commons_file": filename,
                "creator": strip_html((meta.get("Artist") or {}).get("value")) or "unknown",
                "license": "cc0" if lowered.startswith("cc0") else "pd",
                "license_version": "1.0" if lowered.startswith("cc0") else "",
                "license_text": short, "license_url": strip_html((meta.get("LicenseUrl") or {}).get("value")),
                "landing_url": info.get("descriptionurl") or info["url"], "url": info["url"],
                "width": int(info.get("width") or 0), "height": int(info.get("height") or 0),
                "mime": "image/jpeg", "bytes": info.get("size"), "api_sha1": info.get("sha1"),
                "origin": "commons",
                "text": " ".join([filename, strip_html((meta.get("ImageDescription") or {}).get("value")),
                                  strip_html((meta.get("Categories") or {}).get("value"))]).lower(),
            })
    return found


# --- Selection ----------------------------------------------------------

def dedupe_key(candidate):
    return urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(candidate["url"]).path)).lower()


def rank_key(cell_id, candidate):
    """Deterministic, content-independent order (not alphabetical, not newest-first)."""
    return hashlib.sha1(("%s:%s:%s" % (cell_id, candidate["source"], candidate["id"])).encode()).hexdigest()


def acceptable(candidate, words):
    if max(candidate["width"], candidate["height"]) < MIN_LONG or min(candidate["width"], candidate["height"]) < MIN_SHORT:
        return False
    if any(bad in candidate["title"].lower() for bad in TITLE_BLOCKLIST):
        return False
    return re.search(r"\b(?:%s)s?\b" % "|".join(map(re.escape, words)), candidate["text"]) is not None


def download_verified(candidate):
    """Download the photo; return (bytes, (w, h)) or raise fetcher.FetchError."""
    data = fetcher.http_get(candidate["url"])
    size = jpeg_size(data)
    if not size:
        raise fetcher.FetchError("not a readable JPEG")
    if max(size) < MIN_LONG or min(size) < MIN_SHORT:
        raise fetcher.FetchError("real size %dx%d below minimum" % size)
    if candidate["api_sha1"] and hashlib.sha1(data).hexdigest() != candidate["api_sha1"]:
        raise fetcher.FetchError("SHA-1 differs from the one the Commons API reported")
    return data, size


def slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")[:40]


def fill_cell(run, cell, state):
    cell_id, subject, lighting, framing, query, words = cell
    ov = openverse_candidates(run, query)
    cm = commons_candidates(run, query)
    pool, seen = [], set()
    for candidate in sorted(ov + cm, key=lambda c: rank_key(cell_id, c)):
        key = dedupe_key(candidate)
        if key in seen or key in state["used"] or not acceptable(candidate, words):
            continue
        seen.add(key)
        pool.append(candidate)
    state["cell_log"].append((cell_id, query, len(ov), len(cm), len(pool)))
    tries = 0
    for candidate in pool:
        if state["creators"].get(candidate["creator"], 0) >= MAX_PER_CREATOR:
            continue
        if tries >= TRIES_PER_CELL:
            break
        tries += 1
        try:
            data, size = download_verified(candidate)
        except fetcher.FetchError as err:
            run.note("%s: skipped %s %s: %s" % (cell_id, candidate["source"], candidate["id"], err))
            continue
        n = len(state["photos"]) + 1
        photo = {k: v for k, v in candidate.items() if k not in ("text", "api_sha1")}
        photo.update({
            "n": n, "cell": cell_id, "subject": subject, "lighting": lighting, "framing": framing,
            "query": query, "width": size[0], "height": size[1], "bytes": len(data),
            "sha256": fetcher.sha256_hex(data),
            "filename": "%02d-%s-%s.jpg" % (n, candidate["source"], slug(candidate["id"])),
            "attribution": '"%s" by %s, %s, %s' % (candidate["title"], candidate["creator"],
                                                   candidate["license_text"], candidate["landing_url"]),
        })
        state["photos"].append(photo)
        state["used"].add(dedupe_key(candidate))
        state["creators"][candidate["creator"]] = state["creators"].get(candidate["creator"], 0) + 1
        return True
    state["unfilled"].append((cell_id, subject, lighting, framing, query, len(pool)))
    return False


def select_photos(run):
    state = {"photos": [], "used": set(), "creators": {}, "cell_log": [], "unfilled": [], "skipped_for_time": []}
    for cell in GRID:
        if run.over_budget():
            state["skipped_for_time"].append(cell[0])
            continue
        fill_cell(run, cell, state)
    return state


# --- Report -------------------------------------------------------------

def table(headers, rows):
    def clean(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(clean(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def fmt_count(value):
    if value is None:
        return "NOT READ (request failed)"
    if value == 0:
        return "0 (zero: failed read, not a finding)"
    return "{:,}".format(int(value))


def read_section(run):
    out = ["## What was read", "",
           "As-of date (UTC): **%s**" % run.as_of, "",
           "Sources visited: Openverse API (%s), Wikimedia Commons API (%s)." % (OPENVERSE, COMMONS),
           "Other sources in the next section were not queried (they need keys or have unclear terms).", "",
           "Candidate counts per source and route (CC0 / public-domain filter applied in each query):", ""]
    rows = [(s, r, q, f, fmt_count(c)) for s, r, q, f, c in run.counts]
    out.append(table(["Source", "Route", "Query / category", "Filter", "Count"], rows))
    out.append("")
    if run.stats:
        total = sum(int(s.get("media_count") or 0) for s in run.stats)
        top = ", ".join("%s %s" % (s.get("source_name"), "{:,}".format(int(s.get("media_count") or 0))) for s in run.stats[:8])
        out.append("Openverse stats route (`/v1/images/stats/`, all licenses, before any filter): %d sources, %s images in total. Largest: %s." % (
            len(run.stats), "{:,}".format(total), top))
    else:
        out.append("Openverse stats route (`/v1/images/stats/`): NOT READ.")
    out.append("")
    ov = next((c for s, r, q, f, c in run.counts if r == "search API, source=wikimedia" and q == "family"), None)
    cm = [c for s, r, q, f, c in run.counts if s.startswith("Wikimedia") and r.startswith("search") and q == "family"]
    if ov is not None and cm and None not in cm:
        out.append("Where routes disagree: for \"family\", Openverse reports %s CC0/PDM Wikimedia-sourced photographs, "
                   "while Commons' own search reports %s files across %s. They count different things "
                   "(Openverse's license filter and 'photograph' category versus Commons categories and bitmap files), "
                   "so neither is a subset of the other; Commons' own search was used for Commons candidates." % (
                       "{:,}".format(ov), " + ".join("{:,}".format(c) for c in cm),
                       " and ".join("incategory:" + c for c in COMMONS_LICENSE_CATEGORIES)))
    out.append("")
    out.append("Candidate pools per grid cell (raw API hits, then after resolution / keyword / duplicate filters):")
    out.append("")
    out.append(table(["Cell", "Search terms", "Openverse hits", "Commons hits", "Usable"], run.state["cell_log"]))
    return "\n".join(out)


def sources_section():
    rows = [
        ("Openverse (api.openverse.org)", "Aggregator; per-item license field (CC0 1.0, PDM 1.0 kept here)",
         "Yes for CC0/PDM; the upstream site's own terms are still on the landing page", "None required for CC0/PDM",
         "Yes, anonymous JSON API, rate limited", "Check upstream landing page per photo"),
        ("Wikimedia Commons", "Per-file license templates (CC0, PD-self, other PD)",
         "Yes for CC0 and PD-self; other PD tags vary by country", "None for CC0/PD; keep the file page link",
         "Yes, MediaWiki API with a User-Agent header, SHA-1 in the API",
         "Personality / model rights are not covered by the copyright license"),
        ("StockSnap (via Openverse source filter)", "CC0 1.0 as listed by Openverse", "Yes", "None",
         "Through Openverse only; not queried directly", "Model releases not stated"),
        ("Unsplash", "Unsplash License (not CC0)", "Unclear: free use, but no compiling into a competing library",
         "Not required", "Official API needs a key; not queried", "RIGHTS UNCLEAR for committing to a repository"),
        ("Pexels", "Pexels License (not CC0)", "Unclear for redistribution of unmodified files", "Not required",
         "API needs a key; not queried", "RIGHTS UNCLEAR"),
        ("Pixabay", "Pixabay Content License (not CC0)", "Unclear for redistribution as-is; identifiable people carry extra limits",
         "Not required", "API needs a key; not queried", "RIGHTS UNCLEAR"),
        ("Team-shot photos", "Owned by the team", "Yes, with written releases from every person shown", "None",
         "Not scriptable (manual upload)", "Needs releases, especially for children"),
    ]
    note = ("Rows other than Openverse and Wikimedia Commons describe the sources' published terms as understood "
            "when this script was written; this run did not read or verify them.")
    return "\n".join(["## Candidate sources", "", table(
        ["Source", "License", "Commit and reuse clearly allowed?", "Attribution", "Scriptable fetch?", "Rights flag"], rows),
        "", note])


def coverage_section(run):
    photos, state = run.state["photos"], run.state
    out = ["## Coverage mix", "",
           "Labels come from the grid cell a photo filled: the search terms plus a keyword check on the "
           "title, tags, description and categories. **No photo was inspected visually**, so subject, lighting and "
           "framing are unverified metadata-based labels.", ""]
    for name, values, key in (("Subject", SUBJECTS, "subject"), ("Lighting", LIGHTING, "lighting"), ("Framing", FRAMING, "framing")):
        out.append("%s: %s" % (name, ", ".join("%s %d" % (v, sum(p[key] == v for p in photos)) for v in values)))
        out.append("")
    unfilled = {u[0]: u for u in state["unfilled"]}
    in_grid = {(c[1], c[2]) for c in GRID}
    gaps = []
    for s in SUBJECTS:
        for l in LIGHTING:
            if any(p["subject"] == s and p["lighting"] == l for p in photos):
                continue
            empty = [u for u in state["unfilled"] if u[1] == s and u[2] == l]
            if empty:
                gaps.append((s, l, "grid cell %s found no usable candidate (%d after filters)" % (empty[0][0], empty[0][5])))
            elif (s, l) in in_grid:
                gaps.append((s, l, "grid cell skipped: time budget reached"))
            else:
                gaps.append((s, l, "not in the 20-cell grid; 20 photos cannot cover all 60 combinations"))
    out.append("Gaps (subject x lighting combinations with no photo):")
    out.append("")
    out.append(table(["Subject", "Lighting", "Reason"], gaps))
    if unfilled:
        out += ["", "Unfilled cells: " + ", ".join(sorted(unfilled))]
    return "\n".join(out)


def recommended_section(run):
    photos = run.state["photos"]
    rows = [(p["n"], "%s:%s (%s)" % (p["source"], p["id"], p["landing_url"]), p["creator"],
             "%s (api: %s %s)" % (p["license_text"], p["license"], p["license_version"]), p["attribution"],
             p["subject"], p["lighting"], p["framing"], "%dx%d" % (p["width"], p["height"])) for p in photos]
    head = ["## Recommended set", "",
            "%d of %d target photos selected. Selection is pinned in `docs/test-photo-set-manifest.json` "
            "(ID, URL, license, SHA-256, as-of date %s); a rerun of the fetch script retrieves exactly these." % (
                len(photos), len(GRID), run.as_of), ""]
    return "\n".join(head) + table(
        ["#", "ID / URL", "Creator", "License", "Attribution", "Subject", "Lighting", "Framing", "Resolution"], rows)


RISKS = """## Rights risks

- A CC0 or public-domain tag covers copyright only. It does not give a model release for identifiable people, and none of the APIs state whether a release exists. Children are the sensitive case: a parent or the uploader may have posted the photo without a signed release.
- Photos here whose subject is a child, a group or adults with children should be treated as unreleased until a person has checked the source page. Prefer silhouettes, backs of heads and distant shots; avoid close-up faces of children where no release is stated.
- Public-domain flags on Commons other than CC0 and PD-self depend on country and date; this script only accepts CC0, 'Public domain' and PD-* short names, and a human should confirm the individual file page.
- Avoid photos with visible brand logos, artwork, house numbers or licence plates (property concerns), and avoid anything from Unsplash, Pexels or Pixabay in the repository until their redistribution terms are reviewed.
- Aggregators such as Openverse can lag behind upstream license changes; the landing URL recorded for each photo is the place to recheck."""


def fetch_section():
    return """## Fetch script

- Script: `docs/fetch_test_photos.py` (standard library only); input `docs/test-photo-set-manifest.json`.
- Run: `python docs/fetch_test_photos.py [--dest test-photos] [--manifest PATH]`.
- Downloads each photo by its source ID/URL, verifies the SHA-256 recorded in the manifest, and writes `ATTRIBUTION.txt` beside the photos.
- Rerunning keeps files that already match their checksum; downloads retry on network errors, 429 and 5xx; a changed URL falls back to Commons `Special:FilePath` or the Openverse detail endpoint; mismatching or missing photos make the exit status non-zero and are listed.
- The manifest is regenerated by `python scripts/survey_test_photos.py`, which also rewrites this document. Because the live APIs change, regenerating can pick different photos; commit the manifest to keep the set fixed.
- Limitation: the checksums were taken at survey time from the URL the APIs gave; they were not cross-checked against a second independent copy except for Commons' own SHA-1."""


OPEN_QUESTIONS = """## Open questions

- Round 2 (visual review): does a person agree with each photo's subject, lighting and framing label, and with the child-related rights judgement?
- Round 3 (rights): is a CC0 tag with no model release acceptable for photos of identifiable children, or should those cells use silhouettes or team-shot photos?
- Round 4 (sources): should Unsplash, Pexels or Pixabay be reviewed with API keys, or are CC0/PD sources enough?
- Round 5 (storage): commit the 20 JPEGs to the repository, or keep only the manifest and fetch on demand?"""


def build_report(run):
    photos = run.state["photos"]
    banner = []
    numeric = [c for *_, c in run.counts if c is not None]
    if not numeric or not any(numeric):
        banner.append("**FAILED READ**: every candidate count was missing or zero; the APIs were unreachable or "
                      "answered with errors, so nothing below describes what the sources hold.")
    if len(photos) < len(GRID):
        banner.append("**Partial result**: %d of %d photos selected; see Coverage mix for the cells left unfilled." % (len(photos), len(GRID)))
    if run.state["skipped_for_time"]:
        banner.append("Time budget reached; cells skipped: %s." % ", ".join(run.state["skipped_for_time"]))
    failures = [n for n in run.notes]
    if failures:
        banner.append("Run notes (requests that failed or candidates rejected; the run carried on): %d. First entries:\n"
                      % len(failures) + "\n".join("  - " + n for n in failures[:15]))
    parts = ["# Test photo set survey (license-filtered API route)", ""]
    if banner:
        parts += banner + [""]
    parts += [read_section(run), "", sources_section(), "", recommended_section(run), "", coverage_section(run), "",
              RISKS, "", fetch_section(), "", OPEN_QUESTIONS, ""]
    return "\n".join(parts)


def main():
    run = Run()
    for term in COUNT_TERMS:
        openverse_count(run, term)
        for category in COMMONS_CATEGORIES:
            commons_count(run, term, category)
    for source in COUNT_SOURCES:
        openverse_count(run, "family", source=source)
    openverse_stats(run)
    commons_category_counts(run)
    run.state = select_photos(run)
    photos = run.state["photos"]
    if photos:
        manifest = {"as_of": run.as_of, "target_count": len(GRID), "expected_count": len(photos),
                    "licenses_accepted": "CC0 1.0, Public Domain Mark 1.0, Commons public-domain tags",
                    "photos": photos}
        with open(MANIFEST_PATH, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    report = build_report(run)
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write(report)
    print(report)
    print("\nWrote %s and %s" % (REPORT_RELATIVE, os.path.relpath(MANIFEST_PATH, ROOT)))
    return 0 if photos else 1


if __name__ == "__main__":
    sys.exit(main())
