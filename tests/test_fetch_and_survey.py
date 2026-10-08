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

import fetch_test_photos as ftp  # noqa: E402
import survey_test_photos as survey  # noqa: E402

# Smallest useful JPEG header: SOI, SOF0 with 1200 x 900, then EOI.
JPEG = b"\xff\xd8\xff\xc0\x00\x11\x08\x03\x84\x04\xb0\x03" + b"\x01\x22\x00\x02\x11\x01\x03\x11\x01" + b"\xff\xd9"


def photo(n, data=JPEG, pinned=True):
    return {"slot": "slot-%02d" % n, "id": "loc:%d" % n, "item_url": "https://www.loc.gov/item/%d/" % n,
            "image_url": "https://tile.loc.gov/%d.jpg" % n, "attribution": "Someone, Title, LoC",
            "rights_text": "No known restrictions on publication.",
            "sha256": hashlib.sha256(data).hexdigest() if pinned else None}


class JpegTests(unittest.TestCase):
    def test_size(self):
        self.assertEqual(ftp.jpeg_size(JPEG), (1200, 900))

    def test_not_jpeg(self):
        self.assertIsNone(ftp.jpeg_size(b"<html>error</html>"))


class FetchTests(unittest.TestCase):
    def test_validate_requires_twenty_distinct(self):
        self.assertTrue(ftp.validate_selection([photo(1)]))
        self.assertEqual(ftp.validate_selection([photo(i) for i in range(20)]), [])
        self.assertTrue(ftp.validate_selection([photo(1)] * 20))

    def test_download_then_cached(self):
        item = photo(1)
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ftp, "http_get", return_value=JPEG) as get:
            self.assertEqual(ftp.fetch_one(item, tmp, log=lambda m: None)[0], "ok-downloaded")
            self.assertEqual(ftp.fetch_one(item, tmp, log=lambda m: None)[0], "ok-cached")
            self.assertEqual(get.call_count, 1)

    def test_checksum_mismatch_fails_and_leaves_no_file(self):
        item = photo(1)
        item["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ftp, "http_get", return_value=JPEG):
            status, detail = ftp.fetch_one(item, tmp, log=lambda m: None)
            self.assertEqual(status, "failed")
            self.assertIn("mismatch", detail)
            self.assertEqual(os.listdir(tmp), [])

    def test_error_page_fails(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ftp, "http_get", return_value=b"<html>"):
            self.assertEqual(ftp.fetch_one(photo(1), tmp, log=lambda m: None)[0], "failed")

    def test_network_error_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ftp, "http_get", side_effect=RuntimeError("boom")):
            self.assertEqual(ftp.fetch_one(photo(1), tmp, log=lambda m: None), ("failed", "boom"))

    def test_attribution_lists_every_photo(self):
        text = ftp.attribution_text([photo(i) for i in range(3)])
        self.assertEqual(text.count("Someone, Title, LoC"), 3)

    def test_load_selection_from_document_block(self):
        photos = [photo(i) for i in range(20)]
        block = "text\n```json selection\n" + json.dumps({"photos": photos}) + "\n```\n"
        with tempfile.TemporaryDirectory() as tmp:
            doc = os.path.join(tmp, "doc.md")
            with open(doc, "w") as handle:
                handle.write(block)
            loaded = ftp.load_selection(path=os.path.join(tmp, "missing.json"), doc_path=doc)
        self.assertEqual(len(loaded), 20)


class SurveyTests(unittest.TestCase):
    def test_rights_check(self):
        self.assertTrue(survey.rights_ok(["No known restrictions on publication."]))
        self.assertFalse(survey.rights_ok(["Copyright protected. Permission required."]))
        self.assertFalse(survey.rights_ok([]))

    def test_rights_statements_found_by_key(self):
        item = {"item": {"rights_advisory": ["No known restrictions on publication."], "title": "x"}}
        self.assertEqual(survey.rights_statements(item), ["No known restrictions on publication."])

    def test_creator_formatting(self):
        item = {"item": {"contributor_names": ["Lee, Russell, photographer", "Farm Security Administration"]}}
        self.assertEqual(survey.creator_of(item, {}), "Russell Lee")

    def test_selection_order_is_not_alphabetical(self):
        urls = ["https://www.loc.gov/item/%d/" % i for i in range(10)]
        ordered = sorted(urls, key=lambda u: survey.sha1_key("child-01", u))
        self.assertNotEqual(ordered, sorted(urls))
        self.assertEqual(ordered, sorted(urls, key=lambda u: survey.sha1_key("child-01", u)))

    def test_slots_cover_twenty(self):
        self.assertEqual(len(survey.SLOTS), 20)
        self.assertEqual(len({s[0] for s in survey.SLOTS}), 20)


if __name__ == "__main__":
    unittest.main()
