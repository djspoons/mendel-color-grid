import hashlib
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "docs"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import fetch_test_photos as fetcher  # noqa: E402
import survey_test_photos as survey  # noqa: E402


def photo(n=1, data=b"abc"):
    return {"n": n, "source": "commons", "id": "1", "commons_file": "A b.jpg", "url": "https://example.org/a.jpg",
            "filename": "%02d-commons-1.jpg" % n, "sha256": hashlib.sha256(data).hexdigest(),
            "attribution": '"A" by B, CC0 1.0 Universal, https://example.org/file',
            "license_text": "CC0 1.0 Universal", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "landing_url": "https://example.org/file"}


class FetchTests(unittest.TestCase):
    def test_download_then_cached(self):
        with tempfile.TemporaryDirectory() as dest:
            with mock.patch.object(fetcher, "http_get", return_value=b"abc") as get:
                self.assertEqual(fetcher.fetch_photo(photo(), dest)[0], "downloaded")
                self.assertEqual(fetcher.fetch_photo(photo(), dest)[0], "cached")
                self.assertEqual(get.call_count, 1)

    def test_checksum_mismatch_fails_and_leaves_no_file(self):
        with tempfile.TemporaryDirectory() as dest:
            with mock.patch.object(fetcher, "http_get", return_value=b"different"):
                status, detail = fetcher.fetch_photo(photo(), dest)
            self.assertEqual(status, "failed")
            self.assertIn("checksum mismatch", detail)
            self.assertEqual(os.listdir(dest), [])

    def test_manifest_count_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "m.json")
            with open(path, "w") as handle:
                json.dump({"expected_count": 2, "photos": [photo()]}, handle)
            with self.assertRaises(ValueError):
                fetcher.load_manifest(path)

    def test_attribution_file(self):
        with tempfile.TemporaryDirectory() as dest:
            path = fetcher.write_attribution([photo()], dest)
            with open(path) as handle:
                self.assertIn("CC0 1.0 Universal", handle.read())


class SurveyTests(unittest.TestCase):
    def test_grid_has_twenty_unique_cells(self):
        self.assertEqual(len(survey.GRID), 20)
        self.assertEqual(len({c[0] for c in survey.GRID}), 20)
        for _, subject, lighting, framing, *_ in survey.GRID:
            self.assertIn(subject, survey.SUBJECTS)
            self.assertIn(lighting, survey.LIGHTING)
            self.assertIn(framing, survey.FRAMING)

    def test_jpeg_size(self):
        sof = b"\xff\xd8\xff\xc0\x00\x11\x08\x03\xe8\x07\xd0" + b"\x00" * 20
        self.assertEqual(survey.jpeg_size(sof), (2000, 1000))
        self.assertIsNone(survey.jpeg_size(b"GIF89a"))

    def test_acceptable_filters_size_and_keywords(self):
        base = {"width": 3000, "height": 2000, "title": "Child on a swing", "text": "child on a swing"}
        self.assertTrue(survey.acceptable(base, ("child",)))
        self.assertFalse(survey.acceptable(dict(base, width=800, height=600), ("child",)))
        self.assertFalse(survey.acceptable(dict(base, text="a person"), ("son",)))

    def test_rank_is_deterministic(self):
        c = {"source": "openverse", "id": "x"}
        self.assertEqual(survey.rank_key("c01", c), survey.rank_key("c01", c))


if __name__ == "__main__":
    unittest.main()
