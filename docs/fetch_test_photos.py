#!/usr/bin/env python3
"""Download the fixed 20-photo public-domain test set and write its attribution file.

Standard library only. Reads the pinned selection written by
scripts/survey_test_photos.py (docs/test-photo-set/selection.json). If that file
is missing, it falls back to the JSON block embedded in
docs/test-photo-set-survey.md.

    python docs/fetch_test_photos.py [--out test-photos] [--verify-only]

Behaviour:
  * downloads each photo from its stable image URL, retrying network errors and
    HTTP 429/5xx with backoff (honouring Retry-After);
  * writes to a .part file and renames it only after the bytes check out
    (JPEG signature, and the pinned sha256 when the selection has one);
  * is idempotent: a file already present with a matching sha256 is not fetched again;
  * fails per photo, not per run: every photo is attempted, failures are listed,
    and the exit status is 1 if the set is not exactly the 20 listed photos;
  * writes ATTRIBUTION.md from the selection (no network needed).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SELECTION_PATH = os.path.join(HERE, "test-photo-set", "selection.json")
SURVEY_DOC_PATH = os.path.join(HERE, "test-photo-set-survey.md")
EXPECTED_COUNT = 20
USER_AGENT = "test-photo-set-fetch/1.0 (public-domain test photo set)"
MAX_ATTEMPTS = 4
TIMEOUT = 60
MAX_BYTES = 60 * 1024 * 1024


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jpeg_size(data):
    """Return (width, height) from a JPEG header, or None if data is not a JPEG."""
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker == 0xFF:
            pos += 1
            continue
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        length = int.from_bytes(data[pos + 2:pos + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        pos += 2 + length
    return None


def http_get(url, retries=MAX_ATTEMPTS, pause=2.0, accept=None, log=None):
    """GET url and return bytes. Retries network errors, 429 and 5xx; raises RuntimeError after."""
    last = "no attempt made"
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        if accept:
            request.add_header("Accept", accept)
        wait = pause * attempt
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise RuntimeError("response larger than %d bytes" % MAX_BYTES)
            return data
        except urllib.error.HTTPError as err:
            last = "HTTP %d" % err.code
            if err.code == 429:
                retry_after = err.headers.get("Retry-After", "")
                wait = min(float(retry_after), 60.0) if retry_after.isdigit() else max(wait, 10.0)
            elif err.code < 500:
                raise RuntimeError("%s for %s" % (last, url))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as err:
            last = "%s: %s" % (type(err).__name__, err)
        if attempt < retries:
            if log:
                log("  retry %d/%d for %s (%s) in %.0fs" % (attempt, retries - 1, url, last, wait))
            time.sleep(wait)
    raise RuntimeError("giving up on %s after %d attempts (%s)" % (url, retries, last))


def load_selection(path=SELECTION_PATH, doc_path=SURVEY_DOC_PATH):
    """Load the pinned photo list from selection.json, else from the survey document."""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    elif os.path.exists(doc_path):
        with open(doc_path, encoding="utf-8") as handle:
            text = handle.read()
        match = re.search(r"```json selection\n(.*?)\n```", text, re.S)
        if not match:
            raise RuntimeError("no selection.json and no embedded selection in %s" % doc_path)
        data = json.loads(match.group(1))
    else:
        raise RuntimeError("no selection found: run scripts/survey_test_photos.py first")
    photos = data["photos"] if isinstance(data, dict) else data
    return photos


def validate_selection(photos):
    """Return a list of problems with the selection (empty when it is exactly 20 distinct photos)."""
    problems = []
    if len(photos) != EXPECTED_COUNT:
        problems.append("selection lists %d photos, expected %d" % (len(photos), EXPECTED_COUNT))
    ids = [p.get("id") for p in photos]
    if len(set(ids)) != len(ids):
        problems.append("selection contains duplicate ids")
    for photo in photos:
        for key in ("id", "slot", "image_url", "item_url", "attribution"):
            if not photo.get(key):
                problems.append("photo %s is missing %r" % (photo.get("id", "?"), key))
    return problems


def filename_for(photo):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(photo["id"])).strip("_")
    return "%s-%s.jpg" % (photo["slot"], safe)


def fetch_one(photo, out_dir, log=print):
    """Ensure the photo is in out_dir and verified. Returns (status, detail)."""
    path = os.path.join(out_dir, filename_for(photo))
    pinned = photo.get("sha256")
    if os.path.exists(path):
        if pinned and sha256_file(path) == pinned:
            return "ok-cached", path
        if not pinned:
            with open(path, "rb") as handle:
                if jpeg_size(handle.read()):
                    return "ok-cached-unpinned", path
        log("  existing file for %s does not verify; fetching again" % photo["id"])
    try:
        data = http_get(photo["image_url"], log=log)
    except RuntimeError as err:
        return "failed", str(err)
    if not jpeg_size(data):
        return "failed", "not a JPEG (changed URL or error page?): %s" % photo["image_url"]
    digest = sha256_bytes(data)
    if pinned and digest != pinned:
        return "failed", "sha256 mismatch: got %s, pinned %s (image changed at source)" % (digest, pinned)
    partial = path + ".part"
    with open(partial, "wb") as handle:
        handle.write(data)
    os.replace(partial, path)
    return ("ok-downloaded" if pinned else "ok-downloaded-unpinned"), path


def attribution_text(photos):
    lines = ["# Attribution for the public-domain test photo set", "",
             "Rights statements were recorded from each item's own record at the as-of date in the selection.", ""]
    for photo in photos:
        lines.append("- **%s** `%s`: %s" % (photo["slot"], filename_for(photo), photo["attribution"]))
        lines.append("  - Item: %s" % photo["item_url"])
        if photo.get("rights_text"):
            lines.append("  - Rights statement: %s (%s)" % (photo["rights_text"], photo.get("rights_url", photo["item_url"])))
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", default="test-photos", help="output directory (default: test-photos)")
    parser.add_argument("--verify-only", action="store_true", help="check files already in --out, download nothing")
    args = parser.parse_args(argv)

    try:
        photos = load_selection()
    except (RuntimeError, ValueError, KeyError) as err:
        print("ERROR: cannot load selection: %s" % err, file=sys.stderr)
        return 2
    problems = validate_selection(photos)
    if problems:
        for problem in problems:
            print("ERROR: %s" % problem, file=sys.stderr)
        return 2

    os.makedirs(args.out, exist_ok=True)
    results = {}
    for photo in photos:
        if args.verify_only:
            path = os.path.join(args.out, filename_for(photo))
            if not os.path.exists(path):
                results[photo["id"]] = ("failed", "missing file")
            elif photo.get("sha256") and sha256_file(path) != photo["sha256"]:
                results[photo["id"]] = ("failed", "sha256 mismatch")
            else:
                results[photo["id"]] = ("ok-cached", path)
        else:
            results[photo["id"]] = fetch_one(photo, args.out)
        print("%-24s %-22s %s" % (photo["slot"], results[photo["id"]][0], results[photo["id"]][1]))

    with open(os.path.join(args.out, "ATTRIBUTION.md"), "w", encoding="utf-8") as handle:
        handle.write(attribution_text(photos))

    failed = [pid for pid, (status, _) in results.items() if status == "failed"]
    good = len(photos) - len(failed)
    print("\n%d/%d photos verified in %s; attribution written to %s"
          % (good, len(photos), args.out, os.path.join(args.out, "ATTRIBUTION.md")))
    if failed:
        print("FAILED: %s" % ", ".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
