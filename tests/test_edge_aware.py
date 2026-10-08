import unittest

import numpy as np

from picture_method import color, config, edge_aware, metrics, render


def two_tone(cols=12, rows=16, s=config.SUPERSAMPLE, left=(20, 20, 20), right=(235, 235, 235)):
    """A work image with a vertical dark/light border in the middle."""
    img = np.zeros((rows * s, cols * s, 3), dtype=np.uint8)
    img[:, : cols * s // 2] = left
    img[:, cols * s // 2:] = right
    return img


class EdgeAwareTests(unittest.TestCase):
    def test_flat_image_uses_no_edge_rule(self):
        work = np.full((16 * 8, 12 * 8, 3), 200, dtype=np.uint8)
        result = edge_aware.color_cells(work, 12, 16)
        self.assertEqual(result.n_edge_cells, 0)
        self.assertEqual(len(np.unique(result.indices)), 1)

    def test_border_cells_take_edge_rule_and_pure_sides(self):
        result = edge_aware.color_cells(two_tone(), 12, 16)
        self.assertGreater(result.n_edge_cells, 0)
        black = color.PALETTE_NAMES.index("Black")
        white = color.PALETTE_NAMES.index("White")
        self.assertTrue((result.indices[:, 0] == black).all())
        self.assertTrue((result.indices[:, -1] == white).all())
        # No blended gray cells appear on the border.
        gray = color.PALETTE_NAMES.index("Gray")
        self.assertFalse((result.indices == gray).any())

    def test_island_removed_when_not_edge_supported(self):
        indices = np.zeros((5, 5), dtype=int)
        indices[2, 2] = 3
        lab = np.zeros((5, 5, 3))
        fixed, changed = edge_aware.remove_islands(indices, np.zeros((5, 5), bool), lab)
        self.assertEqual(fixed[2, 2], 0)
        self.assertTrue(changed[2, 2])

    def test_island_kept_when_edge_supported(self):
        indices = np.zeros((5, 5), dtype=int)
        indices[2, 2] = 3
        edge = np.zeros((5, 5), bool)
        edge[2, 2] = True
        fixed, changed = edge_aware.remove_islands(indices, edge, np.zeros((5, 5, 3)))
        self.assertEqual(fixed[2, 2], 3)
        self.assertEqual(changed.sum(), 0)


class MetricsTests(unittest.TestCase):
    def test_island_and_runs(self):
        grid = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        self.assertEqual(metrics.count_islands(grid), 1)
        self.assertAlmostEqual(metrics.mean_run_length(grid), 9 / 5)  # runs per row: 1 + 3 + 1 = 5

    def test_adjacent_same_share(self):
        grid = np.array([[0, 1], [0, 1]])
        self.assertAlmostEqual(metrics.adjacent_same_share(grid), 0.5)

    def test_palette_stats(self):
        grid = np.array([[0, 0], [1, 2]])
        self.assertEqual(metrics.distinct_crayons(grid), 3)
        self.assertAlmostEqual(metrics.top3_share(grid), 1.0)


class RenderTests(unittest.TestCase):
    def test_blank_grids_share_geometry_and_have_no_color(self):
        rng = np.random.default_rng(0)
        grids = [rng.integers(0, 24, size=(16, 12)) for _ in range(3)]
        blanks = [render.blank_grid_image(g) for g in grids]
        ok, message = render.check_blank_geometry(blanks, 12, 16)
        self.assertTrue(ok, message)

    def test_palette_has_24_unique_entries(self):
        self.assertEqual(len(config.PALETTE), 24)
        self.assertEqual(len({h for _, h in config.PALETTE}), 24)


if __name__ == "__main__":
    unittest.main()
