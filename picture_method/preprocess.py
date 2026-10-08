"""Steps shared by every method: center-crop to 3:4 portrait and split into a grid."""

import numpy as np

DENSITIES = [(24, 32), (36, 48), (48, 64)]  # (columns, rows)


def center_crop_3x4(image):
    """Center-crop a PIL image to 3:4 (width:height).

    Returns (cropped, removed) where removed says which part of the picture was cut
    off: "sides" for landscape/wide sources, "top and bottom" for very tall ones.
    """
    width, height = image.size
    target_width = round(height * 3 / 4)
    if target_width < width:
        left = (width - target_width) // 2
        return image.crop((left, 0, left + target_width, height)), "sides"
    if target_width > width:
        target_height = round(width * 4 / 3)
        top = (height - target_height) // 2
        return image.crop((0, top, width, top + target_height)), "top and bottom"
    return image.copy(), "nothing"


def cell_means(pixels, cols, rows):
    """Split an (H, W, 3) array into cols x rows cells and return each cell's mean color.

    Result has shape (rows, cols, 3). Cell borders fall on rounded pixel edges, so
    every pixel belongs to exactly one cell.
    """
    height, width = pixels.shape[:2]
    if width < cols or height < rows:
        raise ValueError("image is smaller than the grid")
    x_edges = np.linspace(0, width, cols + 1).round().astype(int)
    y_edges = np.linspace(0, height, rows + 1).round().astype(int)
    data = pixels.astype(np.float64)
    sums = np.add.reduceat(np.add.reduceat(data, y_edges[:-1], axis=0), x_edges[:-1], axis=1)
    counts = np.outer(np.diff(y_edges), np.diff(x_edges))[..., None]
    return sums / counts
