import os
import tempfile
import unittest
from unittest import mock

import helpers  # noqa: F401
import selection
import shotlist
import survey


def cand(url, width=4000, height=3000, rank=0, sha1="abc", source="wikimedia-commons", restrictions=""):
    return {"source": source, "id": url, "page_url": "https://example.org/p", "url": url, "title": "t",
            "creator": "c", "license": "CC0", "license_url": "https://example.org/l", "width": width,
            "height": height, "sha1": sha1, "restrictions": restrictions, "rank": rank}


class SurveyTest(unittest.TestCase):
    def setUp(self):
        self.shot_list = shotlist.load_shot_list()
        self.s = survey.Survey(self.shot_list, "2025-01-01", sleep=lambda x: None)

    def test_qualifies_filters_size_and_restrictions(self):
        self.assertTrue(self.s.qualifies(cand("https://a/1.jpg")))
        self.assertFalse(self.s.qualifies(cand("https://a/2.jpg", 1000, 800)))
        self.assertFalse(self.s.qualifies(cand("https://a/3.jpg", width=None)))
        self.assertFalse(self.s.qualifies(cand("https://a/4.jpg", restrictions="personality")))

    def test_choose_prefers_target_size_then_checksum_and_is_distinct(self):
        self.s.candidates = {
            "S01": [cand("https://a/small.jpg", 2500, 1700, rank=0), cand("https://a/big.jpg", 4200, 2800, rank=3)],
            "S02": [cand("https://a/big.jpg", 4200, 2800), cand("https://a/other.jpg", 4100, 3000, rank=5)],
        }
        pins = self.s.choose([])
        by_slot = {p["slot"]: p for p in pins}
        self.assertEqual(by_slot["S01"]["url"], "https://a/big.jpg")
        self.assertEqual(by_slot["S02"]["url"], "https://a/other.jpg")
        self.assertEqual(len(pins), 2)

    def test_existing_pins_are_kept(self):
        self.s.candidates = {"S01": [cand("https://a/new.jpg")]}
        old = {"slot": "S01", "url": "https://a/old.jpg"}
        self.assertEqual(self.s.choose([old])[0]["url"], "https://a/old.jpg")

    def test_failed_reads_are_flagged_at_top(self):
        self.s.per_slot = {"S01": {"commons": {"error": "HTTP 500"}, "openverse": {"error": None}}}
        self.s.check_plausibility()
        self.assertTrue(any("FAILED READ: no Wikimedia Commons" in n for n in self.s.notes))
        self.assertTrue(any("FAILED READ: no Openverse" in n for n in self.s.notes))
        self.assertTrue(any("Commons per-shot queries failed for: S01" in n for n in self.s.notes))

    def test_render_has_required_sections_and_embedded_pins(self):
        self.s.check_plausibility()
        pins = self.s.choose([])
        text = survey.render(self.s, pins, False, False)
        for heading in ("What was read", "Candidate sources", "Recommended set", "Coverage mix", "Rights risks",
                        "Fetch script", "Open questions"):
            self.assertIn("## " + heading, text)
        self.assertTrue(text.index("## What was read") < text.index("## Candidate sources"))
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "doc.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            self.assertEqual(selection.load_selection(path)["pins"], pins)

    def test_http_json_throttle_and_retry(self):
        import urllib.error
        calls = []

        def fake(request, timeout=0):
            calls.append(1)
            raise urllib.error.HTTPError(request.full_url, 429, "slow", {}, None)
        with mock.patch("urllib.request.urlopen", fake):
            with self.assertRaises(survey.Throttled):
                survey.http_json("https://example.org/x", sleep=lambda s: None)
        self.assertEqual(len(calls), 1)

        def flaky(request, timeout=0):
            calls.append(1)
            raise urllib.error.URLError("down")
        calls.clear()
        with mock.patch("urllib.request.urlopen", flaky):
            data, err = survey.http_json("https://example.org/x", retries=3, sleep=lambda s: None)
        self.assertIsNone(data)
        self.assertEqual(len(calls), 3)
        self.assertIn("down", err)


if __name__ == "__main__":
    unittest.main()
