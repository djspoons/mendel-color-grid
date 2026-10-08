import numpy as np
from PIL import Image

from picture_method import metrics, render
from picture_method.average_then_snap import Boost, average_cells, average_then_snap, snap_to_palette
from picture_method.palette import CRAYONS, PALETTE_RGB, srgb_to_lab
from picture_method.preprocess import cell_means, center_crop_3x4


def test_palette_has_24_unique_crayons():
    assert len(CRAYONS) == 24
    assert len({name for name, _ in CRAYONS}) == 24
    assert len({hex_ for _, hex_ in CRAYONS}) == 24


def test_lab_of_white_and_black():
    lab = srgb_to_lab(np.array([[255, 255, 255], [0, 0, 0]]))
    assert np.allclose(lab[0], [100, 0, 0], atol=0.1)
    assert np.allclose(lab[1], [0, 0, 0], atol=0.1)


def test_snap_returns_exact_crayon():
    means = PALETTE_RGB.reshape(4, 6, 3)
    assert (snap_to_palette(means) == np.arange(24).reshape(4, 6)).all()


def test_snap_uses_lab_not_rgb_on_near_color():
    near_red = np.array([[[236, 40, 80]]], dtype=float)
    assert snap_to_palette(near_red)[0, 0] == 0  # Red


def test_center_crop_landscape_removes_sides():
    cropped, removed = center_crop_3x4(Image.new("RGB", (400, 300)))
    assert cropped.size == (225, 300)
    assert removed == "sides"


def test_center_crop_tall_removes_top_and_bottom():
    cropped, removed = center_crop_3x4(Image.new("RGB", (300, 600)))
    assert cropped.size == (300, 400)
    assert removed == "top and bottom"


def test_cell_means_averages_each_cell():
    pixels = np.zeros((4, 4, 3))
    pixels[:2, 2:] = 100
    means = cell_means(pixels, 2, 2)
    assert means.shape == (2, 2, 3)
    assert means[0, 1, 0] == 100 and means[0, 0, 0] == 0 and means[1, 1, 0] == 0


def test_average_then_snap_shape_and_flat_color():
    image = Image.new("RGB", (120, 160), (255, 255, 255))
    grid = average_then_snap(image, 24, 32, Boost(1.0, 1.0))
    assert grid.shape == (32, 24)
    assert (grid == 15).all()  # White
    assert average_cells(image, 24, 32).shape == (32, 24, 3)


def test_island_and_run_metrics():
    grid = np.array([[0, 0, 1], [0, 2, 1], [0, 0, 1]])
    assert metrics.island_count(grid) == 1  # the lone 2
    assert metrics.mean_row_run_length(grid) == 9 / 7
    assert metrics.adjacent_same_share(np.zeros((3, 3), dtype=int)) == 1.0


def test_blank_grid_geometry_is_independent_of_the_picture():
    a = np.zeros((32, 24), dtype=int)
    b = np.random.default_rng(1).integers(0, 24, size=(32, 24))
    assert render.geometry_signature(a, 40) == render.geometry_signature(b, 40)
    assert render.render_blank(b, 40).mode == "L"
