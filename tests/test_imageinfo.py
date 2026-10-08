import unittest

import helpers
import imageinfo


class ImageInfoTest(unittest.TestCase):
    def test_jpeg_size_and_clean(self):
        info = imageinfo.inspect_bytes(helpers.make_jpeg(3000, 2000))
        self.assertEqual((info.width, info.height, info.format), (3000, 2000, "jpeg"))
        self.assertEqual(info.metadata, [])

    def test_jpeg_metadata_detected(self):
        info = imageinfo.inspect_bytes(helpers.make_jpeg(exif=True, xmp=True))
        self.assertEqual(info.metadata, ["EXIF", "XMP"])

    def test_strip_removes_metadata_and_keeps_size(self):
        raw = helpers.make_jpeg(2500, 1700, exif=True, xmp=True)
        clean = imageinfo.strip_jpeg_metadata(raw)
        info = imageinfo.inspect_bytes(clean)
        self.assertEqual(info.metadata, [])
        self.assertEqual((info.width, info.height), (2500, 1700))
        self.assertTrue(clean.endswith(b"\x12\x34\x56\xff\xd9"))
        self.assertLess(len(clean), len(raw))

    def test_png(self):
        info = imageinfo.inspect_bytes(helpers.make_png(2400, 1600, text=True))
        self.assertEqual((info.width, info.height, info.format), (2400, 1600, "png"))
        self.assertEqual(info.metadata, ["PNG text"])

    def test_rejects_non_images(self):
        with self.assertRaises(imageinfo.ImageError):
            imageinfo.inspect_bytes(b"<html>moved</html>")
        with self.assertRaises(imageinfo.ImageError):
            imageinfo.inspect_bytes(b"\xff\xd8\xff")


if __name__ == "__main__":
    unittest.main()
