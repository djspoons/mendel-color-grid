import os
import tempfile
import unittest

import helpers
import shotlist
import validate_photos


class ValidatePhotosTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = self._tmp.name
        self.shot_list = shotlist.load_shot_list()
        self.manifest = helpers.write_valid_submission(self.folder, self.shot_list)

    def tearDown(self):
        self._tmp.cleanup()

    def validate(self, **kwargs):
        return validate_photos.validate_folder(self.folder, self.shot_list, **kwargs)

    def test_valid_folder_passes(self):
        result = self.validate()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["submitted"], 20)
        self.assertEqual(result["actual"]["subject"], result["planned"]["subject"])
        self.assertEqual(validate_photos.main([self.folder]), 0)

    def test_exif_is_an_error(self):
        with open(os.path.join(self.folder, "S01.jpg"), "wb") as handle:
            handle.write(helpers.make_jpeg(exif=True))
        errors = self.validate()["errors"]
        self.assertTrue(any("S01.jpg" in e and "EXIF" in e for e in errors))

    def test_low_resolution_is_an_error(self):
        with open(os.path.join(self.folder, "S02.jpg"), "wb") as handle:
            handle.write(helpers.make_jpeg(1200, 800))
        self.assertTrue(any("S02.jpg" in e and "below the minimum" in e for e in self.validate()["errors"]))

    def test_missing_release_and_checksum_mismatch(self):
        self.manifest["photos"][0]["people"] = [{"release_id": "R-999"}]
        helpers.write_manifest(self.folder, self.manifest)
        self.assertTrue(any("R-999" in e for e in self.validate()["errors"]))
        with open(os.path.join(self.folder, "releases", "R-001.pdf"), "wb") as handle:
            handle.write(b"tampered")
        self.assertTrue(any("R-001" in e and "sha256" in e for e in self.validate()["errors"]))

    def test_child_needs_guardian_release(self):
        self.manifest["photos"][0]["people"] = [{"release_id": "R-001"}]  # adult release only
        helpers.write_manifest(self.folder, self.manifest)
        self.assertTrue(any("child release" in e for e in self.validate()["errors"]))

    def test_missing_shot_and_mix(self):
        self.manifest["photos"].pop()  # S20
        helpers.write_manifest(self.folder, self.manifest)
        errors = self.validate()["errors"]
        self.assertTrue(any("missing shots: S20" in e for e in errors))
        self.assertTrue(any("mix lighting=low_light" in e for e in errors))
        self.assertTrue(any("S20.jpg" in e and "not in the manifest" in e for e in errors))
        partial = self.validate(allow_partial=True)["errors"]
        self.assertFalse(any("missing shots" in e or "mix " in e for e in partial))

    def test_actual_label_changes_mix(self):
        self.manifest["photos"][0]["actual"] = {"lighting": "bright"}
        helpers.write_manifest(self.folder, self.manifest)
        result = self.validate()
        self.assertTrue(any("mix lighting=indoor" in e for e in result["errors"]))
        self.assertTrue(any("plans indoor" in w for w in result["warnings"]))

    def test_cc0_and_bystander_flags(self):
        self.manifest["photos"][3]["cc0_dedicated"] = False
        self.manifest["photos"][4]["bystanders_identifiable"] = True
        helpers.write_manifest(self.folder, self.manifest)
        errors = self.validate()["errors"]
        self.assertTrue(any("cc0_dedicated" in e for e in errors))
        self.assertTrue(any("bystanders_identifiable" in e for e in errors))

    def test_path_escape_rejected(self):
        self.manifest["photos"][0]["file"] = "../outside.jpg"
        helpers.write_manifest(self.folder, self.manifest)
        self.assertTrue(any("inside the folder" in e for e in self.validate()["errors"]))

    def test_unreadable_folder_exit_code(self):
        self.assertEqual(validate_photos.main([os.path.join(self.folder, "nope")]), 2)


if __name__ == "__main__":
    unittest.main()
