#!/usr/bin/env python3
"""Survey open sources as a fallback for the team-shot plan and write the findings document.

Writes docs/test-photo-set-survey.md (and fallback_selection.json beside this script),
printing the document too. Standard library only.

Sources read (no key needed; the optional OPENVERSE_CLIENT_ID / OPENVERSE_CLIENT_SECRET
only lift Openverse's anonymous rate limit):
  * Wikimedia Commons, MediaWiki API: full-text search restricted to Category:CC-Zero,
    and the category's own file count (two routes whose counts are compared).
  * Openverse API: the catalogue statistics endpoint, and licence-filtered search
    (cc0 and pdm).

Picks are pinned: with an existing fallback_selection.json (or an embedded block in the
document) the same photos are kept; pass --refresh to choose again.
"""
import argparse
import datetime
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import selection as selection_mod  # noqa: E402
import shotlist  # noqa: E402

USER_AGENT = "test-photo-set-survey/1.0 (open-licence photo survey; contact: repository owner)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
OPENVERSE_API = "https://api.openverse.org/v1"
OUTPUT_MD = selection_mod.DEFAULT_SURVEY_MD
COMMONS_PAGE_LIMIT = 30
OPENVERSE_PAGE_SIZE = 20
EXPECTED_MIN_CATALOGUE = 1000  # the hop expects thousands per source; fewer means a failed read
GENERIC_QUERY = "family"


class Throttled(Exception):
    pass


def http_json(url, params=None, headers=None, form=None, retries=3, timeout=30, sleep=time.sleep):
    """GET (or POST with form) JSON. Returns (data, None) or (None, reason).

    Retries network errors and 5xx with backoff. A 429 is retried only when the server asks
    for a short wait; otherwise Throttled is raised so the caller can stop querying that source.
    """
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    body = urllib.parse.urlencode(form).encode() if form else None
    reason = "unknown error"
    for attempt in range(retries):
        request = urllib.request.Request(url, data=body, headers=dict(
            {"User-Agent": USER_AGENT, "Accept": "application/json"}, **(headers or {})))
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8")), None
        except urllib.error.HTTPError as exc:
            reason = "HTTP %d" % exc.code
            if exc.code == 429:
                wait = exc.headers.get("Retry-After", "")
                if wait.isdigit() and int(wait) <= 20 and attempt + 1 < retries:
                    sleep(int(wait) + 1)
                    continue
                raise Throttled(reason)
            if exc.code < 500:
                return None, reason
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, ValueError) as exc:
            reason = str(getattr(exc, "reason", exc))
        if attempt + 1 < retries:
            sleep(2 ** attempt)
    return None, reason


def clean_text(value, limit=90):
    text = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit - 1] + "…" if len(text) > limit else text


class Survey:
    """Holds what was read, what failed, and the candidates found per shot."""

    def __init__(self, shot_list, as_of, sleep=time.sleep):
        self.shot_list = shot_list
        self.limits = shot_list["resolution"]
        self.as_of = as_of
        self.sleep = sleep
        self.reads = []       # (source, route, request, count text)
        self.notes = []       # fell back / skipped / failed read, shown at the top
        self.totals = {}      # (source, route) -> int
        self.per_slot = {}    # slot -> {source: {"hits", "returned", "qualifying", "error"}}
        self.candidates = {}  # slot -> list of candidate dicts
        self.openverse_blocked = False
        self.openverse_headers = {}

    # --- candidate helpers -------------------------------------------------
    def qualifies(self, cand):
        w, h = cand.get("width"), cand.get("height")
        if not w or not h:
            return False
        if max(w, h) < self.limits["min_long_edge_px"] or min(w, h) < self.limits["min_short_edge_px"]:
            return False
        return not cand.get("restrictions")

    def _record(self, source, route, request, count):
        self.reads.append((source, route, request, count))

    # --- Wikimedia Commons -------------------------------------------------
    def _commons(self, params):
        try:
            return http_json(COMMONS_API, params)
        except Throttled:
            return None, "throttled (HTTP 429)"

    def read_commons_totals(self):
        data, err = self._commons({
            "action": "query", "list": "search", "srsearch": "incategory:CC-Zero filetype:bitmap",
            "srnamespace": "6", "srlimit": "1", "srinfo": "totalhits", "format": "json"})
        hits = ((data or {}).get("query", {}).get("searchinfo", {}) or {}).get("totalhits")
        self._record("Wikimedia Commons", "search API (incategory:CC-Zero filetype:bitmap)",
                     "list=search", hits if hits is not None else "FAILED: %s" % (err or "no totalhits"))
        if hits is not None:
            self.totals[("commons", "search")] = hits
        data, err = self._commons({
            "action": "query", "prop": "categoryinfo", "titles": "Category:CC-Zero", "format": "json"})
        info = None
        for page in ((data or {}).get("query", {}).get("pages", {}) or {}).values():
            info = page.get("categoryinfo")
        if info is not None:
            self.totals[("commons", "category")] = info.get("files", 0)
            self._record("Wikimedia Commons", "category page (Category:CC-Zero)", "prop=categoryinfo",
                         "%d files, %d subcategories" % (info.get("files", 0), info.get("subcats", 0)))
        else:
            self._record("Wikimedia Commons", "category page (Category:CC-Zero)", "prop=categoryinfo",
                         "FAILED: %s" % (err or "no categoryinfo"))
        data, err = self._commons({
            "action": "query", "list": "search", "srsearch": GENERIC_QUERY + " incategory:CC-Zero filetype:bitmap",
            "srnamespace": "6", "srlimit": "1", "srinfo": "totalhits", "format": "json"})
        hits = ((data or {}).get("query", {}).get("searchinfo", {}) or {}).get("totalhits")
        self._record("Wikimedia Commons", "search API, query '%s'" % GENERIC_QUERY, "list=search",
                     hits if hits is not None else "FAILED: %s" % (err or "no totalhits"))
        if hits is not None:
            self.totals[("commons", "search:" + GENERIC_QUERY)] = hits

    def commons_candidates(self, shot):
        data, err = self._commons({
            "action": "query", "generator": "search", "gsrnamespace": "6", "gsrlimit": str(COMMONS_PAGE_LIMIT),
            "gsrsearch": shot["query"] + " incategory:CC-Zero filetype:bitmap", "gsrinfo": "totalhits",
            "prop": "imageinfo", "iiprop": "url|size|mime|sha1|extmetadata",
            "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist|Restrictions", "format": "json"})
        if data is None:
            return [], None, err
        hits = (data.get("query", {}).get("searchinfo", {}) or {}).get("totalhits")
        out = []
        for page in (data.get("query", {}).get("pages", {}) or {}).values():
            info = (page.get("imageinfo") or [{}])[0]
            meta = info.get("extmetadata", {})
            val = lambda key: (meta.get(key) or {}).get("value", "")  # noqa: E731
            license_name = clean_text(val("LicenseShortName"), 60)
            low = license_name.lower()
            if not (low.startswith("cc0") or "public domain" in low or low.startswith("pd")):
                continue
            if info.get("mime") not in ("image/jpeg", "image/png"):
                continue
            title = page.get("title", "")
            out.append({
                "source": "wikimedia-commons", "id": "%s (pageid %s)" % (title, page.get("pageid")),
                "page_url": info.get("descriptionurl", ""), "url": info.get("url", ""),
                "title": re.sub(r"^File:|\.\w+$", "", title), "creator": clean_text(val("Artist"), 60) or "unknown",
                "license": license_name, "license_url": clean_text(val("LicenseUrl"), 200),
                "width": info.get("width"), "height": info.get("height"), "sha1": info.get("sha1"),
                "restrictions": clean_text(val("Restrictions"), 60), "rank": page.get("index", 999)})
        out.sort(key=lambda c: c["rank"])
        return out, hits, None

    # --- Openverse ---------------------------------------------------------
    def openverse_login(self):
        cid, secret = os.environ.get("OPENVERSE_CLIENT_ID"), os.environ.get("OPENVERSE_CLIENT_SECRET")
        if not (cid and secret):
            self.notes.append("Openverse was read anonymously (no OPENVERSE_CLIENT_ID/SECRET set); "
                              "its anonymous rate limit may stop some per-shot queries.")
            return
        try:
            data, err = http_json(OPENVERSE_API + "/auth_tokens/token/", form={
                "grant_type": "client_credentials", "client_id": cid, "client_secret": secret})
        except Throttled:
            data, err = None, "HTTP 429"
        if data and data.get("access_token"):
            self.openverse_headers = {"Authorization": "Bearer " + data["access_token"]}
        else:
            self.notes.append("Openverse token request failed (%s); continued anonymously." % err)

    def _openverse(self, path, params):
        if self.openverse_blocked:
            return None, "skipped: Openverse throttled earlier in this run"
        try:
            return http_json(OPENVERSE_API + path, params, self.openverse_headers)
        except Throttled:
            self.openverse_blocked = True
            return None, "throttled (HTTP 429)"

    def read_openverse_totals(self):
        data, err = self._openverse("/images/stats/", None)
        if isinstance(data, list):
            total = sum(int(item.get("image_count", 0)) for item in data)
            self.totals[("openverse", "stats")] = total
            top = sorted(data, key=lambda i: -int(i.get("image_count", 0)))[:4]
            self._record("Openverse", "stats endpoint (all licences, %d providers)" % len(data), "/images/stats/",
                         "%d images; largest: %s" % (total, ", ".join(
                             "%s %d" % (i.get("source_name"), i.get("image_count", 0)) for i in top)))
        else:
            self._record("Openverse", "stats endpoint", "/images/stats/", "FAILED: %s" % err)
        for lic in ("cc0", "pdm"):
            data, err = self._openverse("/images/", {"q": GENERIC_QUERY, "license": lic, "category": "photograph",
                                                     "page_size": "1"})
            count = (data or {}).get("result_count")
            self._record("Openverse", "search API, license=%s, q=%s" % (lic, GENERIC_QUERY), "/images/",
                         count if count is not None else "FAILED: %s" % err)
            if count is not None:
                self.totals[("openverse", "search:" + lic)] = count

    def openverse_candidates(self, shot):
        data, err = self._openverse("/images/", {
            "q": shot["query"], "license": "cc0,pdm", "category": "photograph", "extension": "jpg",
            "page_size": str(OPENVERSE_PAGE_SIZE)})
        if data is None:
            return [], None, err
        out = []
        for rank, item in enumerate(data.get("results", [])):
            lic = item.get("license", "")
            version = item.get("license_version") or ""
            name = {"cc0": "CC0", "pdm": "Public Domain Mark"}.get(lic, lic)
            out.append({
                "source": "openverse", "id": item.get("id", ""), "page_url": item.get("foreign_landing_url", ""),
                "url": item.get("url", ""), "title": clean_text(item.get("title"), 70) or "untitled",
                "creator": clean_text(item.get("creator"), 60) or "unknown",
                "license": ("%s %s" % (name, version)).strip(), "license_url": item.get("license_url") or "",
                "width": item.get("width"), "height": item.get("height"), "sha1": None,
                "restrictions": "", "rank": rank})
        return out, data.get("result_count"), None

    # --- per-shot reading and selection -------------------------------------
    def read_shots(self):
        for shot in self.shot_list["shots"]:
            slot = shot["id"]
            self.per_slot[slot] = {}
            pool = []
            for key, fn in (("commons", self.commons_candidates), ("openverse", self.openverse_candidates)):
                cands, hits, err = fn(shot)
                good = [c for c in cands if self.qualifies(c) and c["url"].startswith("https://")]
                self.per_slot[slot][key] = {"hits": hits, "returned": len(cands), "qualifying": len(good),
                                            "error": err}
                pool += good
                if key == "commons":
                    self.sleep(0.5)
            self.candidates[slot] = pool
        failed = sum(1 for s in self.per_slot.values() for v in s.values() if v["error"])
        self._record("Both", "per-shot search, %d shots x 2 sources" % len(self.per_slot), "see Coverage mix",
                     "%d of %d queries failed or were skipped" % (failed, 2 * len(self.per_slot)))

    def choose(self, existing_pins):
        """One pin per shot. Existing pins are kept; new ones prefer meeting the target size,
        then a source-published checksum, then the search engine's relevance rank."""
        pins, used = {}, set()
        for pin in existing_pins:
            pins[pin["slot"]] = pin
            used.add(pin["url"])
        target = self.limits["target_long_edge_px"]
        for shot in self.shot_list["shots"]:
            slot = shot["id"]
            if slot in pins:
                continue
            ranked = sorted(
                (c for c in self.candidates.get(slot, []) if c["url"] not in used),
                key=lambda c: (max(c["width"], c["height"]) < target, not c["sha1"], c["rank"], c["id"]))
            if not ranked:
                continue
            c = ranked[0]
            used.add(c["url"])
            credit = "%s by %s (%s), %s" % (c["title"], c["creator"], c["page_url"], c["license"])
            pins[slot] = {"slot": slot, "source": c["source"], "id": c["id"], "page_url": c["page_url"],
                          "url": c["url"], "title": c["title"], "creator": c["creator"],
                          "license": c["license"], "license_url": c["license_url"], "width": c["width"],
                          "height": c["height"], "sha1": c["sha1"], "attribution": credit,
                          "as_of": self.as_of}
        return [pins[s["id"]] for s in self.shot_list["shots"] if s["id"] in pins]

    # --- failed-read detection ----------------------------------------------
    def check_plausibility(self):
        commons = [self.totals.get(("commons", r)) for r in ("search", "category")]
        if all(v is None for v in commons):
            self.notes.append("FAILED READ: no Wikimedia Commons count could be read (see table). "
                              "Commons candidates below are absent for that reason, not because none exist.")
        elif any(v is not None and v < EXPECTED_MIN_CATALOGUE for v in commons):
            self.notes.append("FAILED READ (suspect): a Commons CC0 count is under %d where thousands are "
                              "expected; treat Commons figures as unreliable." % EXPECTED_MIN_CATALOGUE)
        ov = self.totals.get(("openverse", "stats"))
        cc0 = self.totals.get(("openverse", "search:cc0"))
        if ov is None and cc0 is None:
            self.notes.append("FAILED READ: no Openverse count could be read. Openverse candidates below are "
                              "absent for that reason, not because none exist.")
        elif (ov is not None and ov < EXPECTED_MIN_CATALOGUE) or (cc0 is not None and cc0 < EXPECTED_MIN_CATALOGUE):
            self.notes.append("FAILED READ (suspect): an Openverse count is under %d where thousands are "
                              "expected." % EXPECTED_MIN_CATALOGUE)
        if self.openverse_blocked:
            skipped = [s for s, v in self.per_slot.items() if v.get("openverse", {}).get("error")]
            self.notes.append("Openverse throttled the run; %d of %d per-shot queries got no answer (%s). "
                              "Those shots were covered from Commons only." % (
                                  len(skipped), len(self.per_slot), ", ".join(skipped)))
        failed_commons = [s for s, v in self.per_slot.items() if v.get("commons", {}).get("error")]
        if failed_commons:
            self.notes.append("Commons per-shot queries failed for: %s." % ", ".join(failed_commons))


# --- rendering ---------------------------------------------------------------
def table(headers, rows):
    def esc(cell):
        return str(cell).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(" --- " for _ in headers) + "|"]
    lines += ["| " + " | ".join(esc(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def mix_table(counts):
    rows = []
    for dim, label in (("subject", "Subject"), ("lighting", "Lighting"), ("framing", "Framing")):
        rows.append((label, ", ".join("%s %d" % (v, n) for v, n in counts[dim].items())))
    return table(("Dimension", "Counts"), rows)


def planned_gaps(shots):
    present = {(s["subject"], s["lighting"]) for s in shots}
    gaps = []
    for subject in shotlist.SUBJECTS:
        absent = [l for l in shotlist.LIGHTINGS if (subject, l) not in present]
        if absent:
            gaps.append("%s has no %s shot" % (subject, " / ".join(absent)))
    return gaps


def render(survey, pins, args_refresh, kept):
    sl = survey.shot_list
    shots = sl["shots"]
    res = sl["resolution"]
    by_id = shotlist.shots_by_id(sl)
    pin_by_slot = {p["slot"]: p for p in pins}
    n = len(shots)
    out = ["# Test photo set survey: team-shot photo plan", "",
           "Approach: shoot the %d photos ourselves from a shot list, with a release for everyone shown and a CC0 "
           "dedication; use open sources only as a fallback. Everything below the plan is produced by "
           "`docs/team-shot-plan/survey.py`; do not edit by hand." % n, "",
           "## What was read", "",
           "- As-of date (UTC): **%s**" % survey.as_of,
           "- Local: `docs/team-shot-plan/shot_list.json` (%d shots)" % n,
           "- Sources visited: Wikimedia Commons (MediaWiki API), Openverse (API). Routes and counts:", ""]
    out.append(table(("Source", "Route", "Request", "Count"), survey.reads))
    out.append("")
    if survey.notes:
        out.append("**Run status: not everything was read as planned.**")
        out.append("")
        out += ["- " + note for note in survey.notes]
    else:
        out.append("Run status: every route answered; nothing skipped and no fallback taken.")
    out += ["",
            "Selection: %s." % ("kept the pins already recorded in the repository (rerun picks the same photos; "
                                 "`--refresh` re-chooses)" if kept and not args_refresh else
                                 "chosen in this run and pinned below"),
            "",
            "Where the two Commons routes disagree (search hits vs category files) that is a finding: the search "
            "also reaches files in CC-Zero subcategories and matches by text, the category count covers direct "
            "members only.", "",
            "## Candidate sources", ""]
    out.append(table(
        ("Source", "Licence", "Commit and reuse clearly allowed?", "Attribution", "Scriptable fetch", "Rights flag"),
        [("Team-shot photos (this plan)", "CC0 1.0 dedication by us, plus releases", "Yes, we own the rights and hold releases",
          "None required", "Not needed; `validate_photos.py` checks the folder", "None once releases validate"),
         ("Wikimedia Commons, CC-Zero files", "CC0 1.0 as declared by the uploader", "Yes for the copyright; uploader's claim not verified",
          "None required (courtesy credit recorded)", "Yes, API keyless, descriptive User-Agent needed, SHA-1 published",
          "Unclear for identifiable people: CC0 does not cover personality rights"),
         ("Openverse, licence filter cc0 / pdm", "CC0 1.0 or Public Domain Mark 1.0, as passed on from the provider",
          "CC0 yes; Public Domain Mark is a label, not a waiver, so check the provider",
          "None required (courtesy credit recorded)", "Yes, API; anonymous limits are tight, optional OAuth lifts them; no checksum",
          "Unclear for identifiable people; aggregator, so the provider's own terms are the source of truth"),
         ("Unsplash, Pexels, Pixabay", "Each site's own licence, not CC0", "Not clearly: those licences limit redistributing the photos as a set",
          "Not required, but terms vary", "API keys needed; not read in this run", "Rights unclear for committing a copy; model releases not guaranteed")]))
    out += ["", "The last row comes from those sites' published licence terms and was not machine-checked in this run.", ""]

    out += ["## Recommended set", "",
            "Recommended: the team-shot set below. The photos do not exist yet, so the ID/URL column is the path each "
            "photo takes in the submission folder. Resolution: minimum %dx%d px (long x short edge), target %dx%d px, "
            "%s." % (res["min_long_edge_px"], res["min_short_edge_px"], res["target_long_edge_px"],
                     res["target_short_edge_px"], "/".join(res["formats"])), ""]
    rows = [(s["id"], "photos/%s.jpg (to be shot)" % s["id"], "team photographer, named in manifest.json",
             "CC0 1.0 (CC0-DEDICATION.md + releases)", "None required", s["subject"], s["lighting"], s["framing"],
             ">=%dx%d, target %dx%d" % (res["min_long_edge_px"], res["min_short_edge_px"],
                                        res["target_long_edge_px"], res["target_short_edge_px"]))
            for s in shots]
    out.append(table(("Slot", "ID/URL", "Creator", "License", "Attribution string", "Subject", "Lighting",
                      "Framing", "Resolution"), rows))
    out += ["", "Example scenes:", ""]
    out += ["- **%s** (%s, %s, %s; %d people, %d children): %s" % (
        s["id"], s["subject"], s["lighting"], s["framing"], s["people"], s["minors"], s["scene"]) for s in shots]
    out += ["", "### Fallback pins from open sources", "",
            "Use only if team photos are late. Subject, lighting and framing are what the shot slot asks for, matched by "
            "keyword search; they were **not** checked by eye. `fetch_fallback.py` downloads exactly these pins.", ""]
    if pins:
        out.append(table(("Slot", "Source", "ID", "URL", "Creator", "License", "Attribution string", "Resolution", "As of"),
                         [(p["slot"], p["source"], p["id"], p["url"], p["creator"], p["license"], p["attribution"],
                           "%sx%s" % (p["width"], p["height"]), p["as_of"]) for p in pins]))
    else:
        out.append("No fallback pins: no candidate passed the licence and resolution filters in this run.")
    out += ["", "## Coverage mix", "", "Team-shot plan (all %d shots, counts from the shot list):" % n, "",
            mix_table(shotlist.mix_counts(shots)), ""]
    gaps = planned_gaps(shots)
    out.append("Gaps left in the plan (subject by lighting), each for the same reason: the %d-shot budget keeps one "
               "or two shots per combination, and these combinations were dropped first because they are the "
               "hardest to shoot safely or the least typical of family photos:" % n)
    out += ["", *["- " + g for g in gaps], ""]
    pinned_shots = [by_id[s] for s in by_id if s in pin_by_slot]
    out += ["Fallback pins (%d of %d slots filled):" % (len(pinned_shots), n), "",
            mix_table(shotlist.mix_counts(pinned_shots)), ""]
    unfilled = [s for s in by_id if s not in pin_by_slot]
    if unfilled:
        out.append("Slots with no fallback pin, and why:")
        out.append("")
        for slot in unfilled:
            st = survey.per_slot.get(slot, {})
            why = []
            for src in ("commons", "openverse"):
                v = st.get(src)
                if v is None:
                    why.append("%s not queried" % src)
                elif v["error"]:
                    why.append("%s query failed (%s)" % (src, v["error"]))
                else:
                    why.append("%s: %d returned, %d passed licence/size" % (src, v["returned"], v["qualifying"]))
            out.append("- %s (%s, %s, %s): %s" % (slot, by_id[slot]["subject"], by_id[slot]["lighting"],
                                                   by_id[slot]["framing"], "; ".join(why)))
        out.append("")
    out += ["Per-slot candidates found by search (hits = total matches the source reports; qualifying = licence, "
            "size and file type pass, out of the first page returned):", ""]
    rows = []
    for s in shots:
        st = survey.per_slot.get(s["id"], {})

        def cell(key):
            v = st.get(key)
            if v is None:
                return "not queried"
            if v["error"]:
                return "failed: %s" % v["error"]
            return "%s hits, %d/%d qualifying" % (v["hits"] if v["hits"] is not None else "n/r", v["qualifying"], v["returned"])
        pin = pin_by_slot.get(s["id"])
        rows.append((s["id"], s["query"], cell("commons"), cell("openverse"), pin["source"] if pin else "none"))
    out.append(table(("Slot", "Query", "Commons", "Openverse", "Pinned from"), rows))
    out.append("")

    kids_pins = [p["slot"] for p in pins if by_id[p["slot"]]["minors"] > 0]
    people_pins = [p["slot"] for p in pins if by_id[p["slot"]]["people"] > 0]
    out += ["## Rights risks", "",
            "- Identifiable children: %d of the %d planned shots show children. With our own photos every child has a "
            "release signed by a parent or guardian (`RIGHTS.md`); `validate_photos.py` fails a photo without one."
            % (sum(1 for s in shots if s["minors"]), n),
            "- Open-source fallback: CC0 or public domain covers copyright only. It says nothing about a model release "
            "for the people shown. %d fallback pins are planned to show people (%s) and %d of those show children (%s); "
            "none has a verified release. Avoid committing these; prefer slots with pets or objects, or reshoot."
            % (len(people_pins), ", ".join(people_pins) or "none", len(kids_pins), ", ".join(kids_pins) or "none"),
            "- Uploader claims: a CC0 label on Commons or Openverse is the uploader's statement and may be wrong "
            "(someone else's photo). Pins that rely on it have not been independently verified.",
            "- Public Domain Mark (Openverse `pdm`) is a label, not a legal waiver: prefer CC0 when both exist.",
            "- Avoid: photos with a Commons `Restrictions` note (these are filtered out), minors in swimwear or "
            "private spaces, readable names, addresses, number plates, school crests, and any source licence that "
            "limits redistribution (Unsplash, Pexels, Pixabay terms).",
            "- Release scans hold names and signatures; keep them out of the repository and commit only release ids "
            "and checksums.", ""]
    total_h = sum(item["hours"] for item in sl["schedule"])
    out += ["## Cost and schedule", "",
            table(("Step", "Who", "Hours", "Calendar"), [(i["step"], i["who"], "%.1f" % i["hours"], i["calendar_days"])
                                                         for i in sl["schedule"]]),
            "", "Total effort: **%.1f person-hours** over about 10 calendar days (shoots fit into two weekend-style "
            "days because the golden-hour and evening sessions depend on daylight). Cash cost: no licence fees; phone "
            "cameras suffice; household volunteers are unpaid, as the release says. The 3 hours of validation and "
            "reshoot time is an allowance, not a measured figure. For comparison, the fallback is scripted (minutes to "
            "download) but needs a manual look at 20 pins and still leaves unverified rights, so it cannot replace the "
            "team shoot for people photos." % total_h, "",
            "## Fetch script", "",
            "- Team photos: they do not exist yet, so no script can download them. This variation cannot produce "
            "that part. Check a submitted folder with `python docs/team-shot-plan/validate_photos.py <folder>` "
            "(resolution, metadata stripped, release trail, shot ids, mix counts); strip metadata with "
            "`strip_metadata.py`.",
            "- Fallback photos: `python docs/team-shot-plan/fetch_fallback.py` downloads the %d pinned photos to "
            "`photos/fallback/` and writes `photos/fallback/ATTRIBUTION.txt`. It uses the standard library only, "
            "retries network errors, writes atomically, skips files that already verify (idempotent), checks JPEG/PNG "
            "header, minimum resolution, the pinned SHA-1 (Commons pins) and a SHA-256 lock recorded on first download "
            "in `fallback_checksums.json` (Openverse pins have no source checksum, so they are trusted on first "
            "download), reports failed slots and exits 1 if any failed. Pins read from "
            "`fallback_selection.json` or the block at the end of this document." % len(pins),
            "- Slots without a pin (%s) have nothing to download." % (", ".join(unfilled) or "none"), "",
            "## Open questions", "",
            "- Round 1: Which two or three households can we recruit, and who acts as coordinator for the releases?",
            "- Round 1: Is the %dx%d minimum acceptable, or does the consuming test need larger originals?"
            % (res["min_long_edge_px"], res["min_short_edge_px"]),
            "- Round 2: Should fallback pins of people be allowed at all, given no release can be verified?",
            "- Round 2: Where do release scans live (private store), and who does the rights review?",
            "- Round 3: Are the dropped subject/lighting combinations acceptable, or should a second batch cover them?",
            "- Round 3: Should the fallback pins be eyeballed (subject, lighting, framing) before anyone relies on them?",
            "", "## Pinned fallback selection (machine-readable)", "",
            selection_mod.embed_block({"as_of": survey.as_of, "pins": pins}), ""]
    return "\n".join(out)


def run(args):
    shot_list = shotlist.load_shot_list()
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    survey = Survey(shot_list, as_of)
    survey.openverse_login()
    survey.read_commons_totals()
    survey.read_openverse_totals()
    survey.read_shots()
    survey.check_plausibility()
    existing = []
    if not args.refresh:
        path = selection_mod.find_existing()
        if path:
            existing = selection_mod.load_selection(path)["pins"]
    pins = survey.choose(existing)
    text = render(survey, pins, args.refresh, bool(existing))
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(selection_mod.DEFAULT_JSON, "w", encoding="utf-8") as handle:
        json.dump({"as_of": as_of, "pins": pins}, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(text)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--refresh", action="store_true", help="ignore existing pins and choose again")
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
