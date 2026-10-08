import copy
import unittest

import helpers  # noqa: F401  (puts docs/team-shot-plan on sys.path)
import shotlist


class ShotListTest(unittest.TestCase):
    def setUp(self):
        self.data = shotlist.load_shot_list()

    def test_twenty_valid_shots(self):
        self.assertEqual(len(self.data["shots"]), 20)
        self.assertEqual(shotlist.validate_shot_list(self.data), [])

    def test_mix_counts_cover_every_category(self):
        counts = shotlist.mix_counts(self.data["shots"])
        for dim in counts:
            self.assertEqual(sum(counts[dim].values()), 20)
            self.assertTrue(all(n > 0 for n in counts[dim].values()), dim)

    def test_invalid_label_reported(self):
        bad = copy.deepcopy(self.data)
        bad["shots"][0]["lighting"] = "neon"
        self.assertTrue(any("lighting" in p for p in shotlist.validate_shot_list(bad)))

    def test_people_and_minors_consistent(self):
        for shot in self.data["shots"]:
            if shot["subject"] in ("pets", "objects"):
                self.assertEqual(shot["people"], 0)
            if shot["subject"] == "single_child":
                self.assertEqual((shot["people"], shot["minors"]), (1, 1))


if __name__ == "__main__":
    unittest.main()
