import numpy as np
from PIL import Image

from picture_method import metrics, render
from picture_method.inputs import center_crop_3x4
from picture_method.method import (
    count_votes,
    quantize_pixels,
    quantize_then_vote,
    vote_cells,
)
from picture_method.palette import CRAYONS, palette_lab, palette_rgb, rgb_to_lab


def test_palette_has_24_crayons():
    assert len(CRAYONS) == 24
    assert palette_rgb().shape == (24, 3)


def test_white_is_lab_100():
    assert abs(rgb_to_lab(np.array([255, 255, 255]))[0] - 100) < 0.1


def test_exact_crayon_pixels_map_to_themselves():
    pal = palette_rgb()
    labels = quantize_pixels(pal.reshape(1, 24, 3), palette_lab())
    assert labels.tolist() == [list(range(24))]


def test_majority_beats_average():
    # 6x6 cell: 20 pixels of crayon 0, 16 of crayon 2 -> majority is 0
    labels = np.full((6, 6), 2)
    labels.ravel()[:20] = 0
    counts = count_votes(labels, 1, 1)
    grid, ties = vote_cells(counts)
    assert grid[0, 0] == 0 and ties == 0


def test_tie_goes_to_larger_neighbor_share():
    # Left, middle, right cells; the middle cell is split 18/18 between 3 and 5.
    labels = np.zeros((6, 18), dtype=int)
    labels[:, :6] = 5
    labels[:, 12:] = 5
    mid = labels[:, 6:12]
    mid[:, :3] = 3
    mid[:, 3:] = 5
    counts = count_votes(labels, 3, 1)
    grid, ties = vote_cells(counts)
    assert ties == 1 and grid[0, 1] == 5


def test_crop_is_3_by_4():
    assert center_crop_3x4(Image.new("RGB", (400, 300))).size == (225, 300)
    assert center_crop_3x4(Image.new("RGB", (300, 600))).size == (300, 400)


def test_pipeline_on_solid_color():
    img = Image.new("RGB", (300, 400), tuple(palette_rgb()[2]))
    for dither in (False, True):
        result = quantize_then_vote(img, 6, 8, dither=dither)
        assert result.grid.shape == (8, 6)
        if not dither:
            assert (result.grid == 2).all()


def test_metrics():
    grid = np.array([[0, 0, 1], [2, 0, 1], [2, 3, 1]])
    assert metrics.island_count(grid) == 1  # the 3
    assert metrics.same_adjacent_share(np.zeros((4, 4), dtype=int)) == 1.0
    assert metrics.mean_run_length(np.zeros((2, 5), dtype=int)) == 5.0


def test_blank_grid_is_clean():
    grid = np.arange(24).reshape(4, 6)
    blank = render.render_blank(grid)
    assert render.check_blank(blank, 4, 6)
    assert blank.mode == "L"
