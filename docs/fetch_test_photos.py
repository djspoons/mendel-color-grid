#!/usr/bin/env python3
"""Download the pinned 20-photo family test set and write an attribution file.

Reads docs/test-photo-set-manifest.json (written by scripts/survey_test_photos.py),
downloads each photo by its source ID, verifies its SHA-256 and writes
ATTRIBUTION.txt next to the photos. Standard library only.

    python docs/fetch_test_photos.py [--dest test-photos] [--manifest PATH]

Reruns are idempotent: a file already present with the right checksum is kept.
Exit status is 0 only when every photo in the manifest is present and verified.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MANIFEST = os.path.join(HERE, "test-photo-set-manifest.json")
DEFAULT_DEST = "test-photos"
USER_AGENT = "family-test-photo-fetch/1.0 (stdlib urllib; open-license test set)"
MAX_BYTES = 30 * 1024 * 1024
OPENVERSE_DETAIL = "https://api.openverse.org/v1/images/{}/"
COMMONS_FILE_PATH = "https://commons.wikimedia.org/wiki/Special:FilePath/{}"


class FetchError(Exception):
    """A download that failed for good (after retries where retrying makes sense)."""


def http_get(url, retries=3, timeout=30, max_bytes=MAX_BYTES):
    """GET url and return the body bytes; retry network errors, 429 and 5xx."""
    last = None
    for attempt in range(retries):
        if attempt:
            time.sleep(2 ** attempt)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                length = response.headers.get("Content-Length")
                if length and int(length) > max_bytes:
                    raise FetchError("Content-Length %s exceeds %d bytes" % (length, max_bytes))
                body = response.read(max_bytes + 1)
                if len(body) > max_bytes:
                    raise FetchError("body exceeds %d bytes" % max_bytes)
                return body
        except urllib.error.HTTPError as err:
            last = "HTTP %d" % err.code
            if err.code != 429 and err.code < 500:
                break  # 404 and friends will not get better
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as err:
            last = "%s: %s" % (type(err).__name__, err)
    raise FetchError("%s (%s)" % (url, last))


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def candidate_urls(photo):
    """The recorded URL first, then a source-specific way to find the file again."""
    yield photo["url"]
    try:
        if photo["source"] == "commons":
            yield COMMONS_FILE_PATH.format(urllib.parse.quote(photo["commons_file"]))
        elif photo["source"] == "openverse":
            detail = json.loads(http_get(OPENVERSE_DETAIL.format(photo["id"])).decode("utf-8"))
            if detail.get("url"):
                yield detail["url"]
    except (FetchError, ValueError, KeyError):
        return


def fetch_photo(photo, dest):
    """Return (status, detail); status is 'cached', 'downloaded' or 'failed'."""
    path = os.path.join(dest, photo["filename"])
    if os.path.isfile(path):
        with open(path, "rb") as handle:
            if sha256_hex(handle.read()) == photo["sha256"]:
                return "cached", path
    problems = []
    for url in candidate_urls(photo):
        try:
            data = http_get(url)
        except FetchError as err:
            problems.append(str(err))
            continue
        if sha256_hex(data) != photo["sha256"]:
            problems.append("checksum mismatch from %s" % url)
            continue
        tmp = path + ".part"
        with open(tmp, "wb") as handle:
            handle.write(data)
        os.replace(tmp, path)
        return "downloaded", path
    return "failed", "; ".join(problems) or "no URL to try"


def attribution_line(photo):
    return "%02d. %s\n    File: %s\n    License: %s <%s>\n    Source: %s" % (
        photo["n"], photo["attribution"], photo["filename"],
        photo["license_text"], photo["license_url"], photo["landing_url"])


def write_attribution(photos, dest):
    path = os.path.join(dest, "ATTRIBUTION.txt")
    lines = ["Attribution for the family test photo set (CC0 / public domain).",
             "Attribution is not legally required for these licenses; it is kept for provenance.",
             ""]
    lines += [attribution_line(p) + "\n" for p in photos]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return path


def load_manifest(path):
    with open(path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    photos = manifest.get("photos", [])
    expected = manifest.get("expected_count")
    if expected is None or len(photos) != expected:
        raise ValueError("manifest lists %d photos, expected %s" % (len(photos), expected))
    names = [p["filename"] for p in photos]
    if len(set(names)) != len(names):
        raise ValueError("manifest has duplicate filenames")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--dest", default=DEFAULT_DEST)
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
    except (OSError, ValueError) as err:
        print("cannot use manifest %s: %s" % (args.manifest, err), file=sys.stderr)
        return 2
    os.makedirs(args.dest, exist_ok=True)
    ok, failed = [], []
    for photo in manifest["photos"]:
        status, detail = fetch_photo(photo, args.dest)
        print("%02d %-10s %s%s" % (photo["n"], status, photo["filename"],
                                   "" if status != "failed" else "  -> " + detail))
        (failed if status == "failed" else ok).append(photo)
    attribution = write_attribution(ok, args.dest)
    print("verified %d/%d photos in %s; attribution: %s" % (
        len(ok), len(manifest["photos"]), args.dest, attribution))
    if failed:
        print("FAILED: " + ", ".join(p["filename"] for p in failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
