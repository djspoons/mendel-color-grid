import hashlib
import json
import os
import tempfile
import unittest
from unittest import mock

import helpers
import fetch_fallback
import selection

LIMITS = {"min_long_edge_px": 2400, "min_short_edge_px": 1600}
GOOD = helpers.make_jpeg(3000, 2000)


def pin(slot, url, data=GOOD, with_sha1=True):
    return {"slot": slot, "source": "wikimedia-commons", "id": "File:" + slot, "page_url": "https://example.org/" + slot,
            "url": url, "title": slot, "creator": "Someone", "license": "CC0", "license_url": "https://example.org/cc0",
            "width": 3000, "height": 2000, "sha1": hashlib.sha1(data).hexdigest() if with_sha1 else None,
            "attribution": "%s by Someone, CC0" % slot, "as_of": "2025-01-01"}


class FetchFallbackTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.out = os.path.join(self._tmp.name, "out")
        self.lock = os.path.join(self._tmp.name, "lock.json")
        self.sel = {"as_of": "2025-01-01", "pins": [pin("S01", "https://example.org/a.jpg"),
                                                     pin("S02", "https://example.org/b.jpg")]}

    def tearDown(self):
        self._tmp.cleanup()

    def run_fetch(self, downloader):
        with mock.patch.object(fetch_fallback, "download", side_effect=downloader):
            return fetch_fallback.run(self.sel, self.out, self.lock, LIMITS, 20, sleep=lambda s: None,
                                      log=lambda m: None)

    def test_downloads_writes_attribution_and_lock(self):
        ok, failures = self.run_fetch(lambda url, *a: GOOD)
        self.assertEqual((ok, failures), (2, {}))
        self.assertTrue(os.path.isfile(os.path.join(self.out, "S01_wikimedia-commons.jpg")))
        text = open(os.path.join(self.out, "ATTRIBUTION.txt"), encoding="utf-8").read()
        self.assertIn("S01 by Someone, CC0", text)
        self.assertEqual(len(json.load(open(self.lock))), 2)

    def test_rerun_is_idempotent(self):
        self.run_fetch(lambda url, *a: GOOD)
        calls = []
        ok, failures = self.run_fetch(lambda url, *a: calls.append(url) or GOOD)
        self.assertEqual((ok, failures, calls), (2, {}, []))

    def test_failures_do_not_stop_the_rest(self):
        def downloader(url, *a):
            if url.endswith("a.jpg"):
                raise fetch_fallback.FetchError("download failed after 3 attempt(s): HTTP 404")
            return GOOD
        ok, failures = self.run_fetch(downloader)
        self.assertEqual(ok, 1)
        self.assertIn("HTTP 404", failures["S01"])
        self.assertIn("S02", open(os.path.join(self.out, "ATTRIBUTION.txt")).read())
        self.assertNotIn("S01_", open(os.path.join(self.out, "ATTRIBUTION.txt")).read())

    def test_changed_content_is_rejected(self):
        ok, failures = self.run_fetch(lambda url, *a: helpers.make_jpeg(3001, 2000))
        self.assertEqual(ok, 0)
        self.assertTrue(all("SHA-1" in r for r in failures.values()))
        self.assertFalse(os.path.exists(os.path.join(self.out, "S01_wikimedia-commons.jpg")))

    def test_html_page_and_small_image_rejected(self):
        self.sel["pins"][0]["sha1"] = None
        self.sel["pins"][1]["sha1"] = None
        ok, failures = self.run_fetch(lambda url, *a: b"<html>gone</html>" if url.endswith("a.jpg")
                                      else helpers.make_jpeg(800, 600))
        self.assertEqual(ok, 0)
        self.assertIn("not a usable image", failures["S01"])
        self.assertIn("below the minimum", failures["S02"])

    def test_lock_detects_later_change_without_source_checksum(self):
        for p in self.sel["pins"]:
            p["sha1"] = None
        self.run_fetch(lambda url, *a: GOOD)
        for name in os.listdir(self.out):
            if name.endswith(".jpg"):
                os.remove(os.path.join(self.out, name))
        ok, failures = self.run_fetch(lambda url, *a: helpers.make_jpeg(3500, 2000))
        self.assertEqual(ok, 0)
        self.assertTrue(all("lock file" in r for r in failures.values()))

    def test_download_retries_then_reports(self):
        import urllib.error
        attempts = []

        def fake_open(request, timeout=0):
            attempts.append(1)
            raise urllib.error.HTTPError(request.full_url, 503, "busy", {}, None)
        with mock.patch("urllib.request.urlopen", fake_open):
            with self.assertRaises(fetch_fallback.FetchError) as ctx:
                fetch_fallback.download("https://example.org/x.jpg", 5, 3, sleep=lambda s: None)
        self.assertEqual(len(attempts), 3)
        self.assertIn("HTTP 503", str(ctx.exception))

    def test_selection_round_trip_through_markdown(self):
        path = os.path.join(self._tmp.name, "survey.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("# doc\n\n" + selection.embed_block(self.sel) + "\n")
        self.assertEqual(selection.load_selection(path)["pins"], self.sel["pins"])

    def test_local_name_rejects_odd_extension(self):
        with self.assertRaises(fetch_fallback.FetchError):
            fetch_fallback.local_name(pin("S01", "https://example.org/a.svg"))


if __name__ == "__main__":
    unittest.main()
