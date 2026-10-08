"""Edge-aware cell coloring.

Steps (each is its own function so they can be ported or compared separately):
  1. cell_blocks            - split the supersampled image into per-cell pixel blocks
  2. edge_strength          - Sobel magnitude on a luminance copy, averaged per cell
  3. edge_cell_mask         - flag the strongest-edge cells
  4. flat_cell_colors       - mean of the block in Lab, snapped to the nearest crayon
  5. edge_cell_colors       - dominant crayon of the darker or lighter side of the edge
  6. remove_islands         - drop single-cell islands that no edge supports
"""

from dataclasses import dataclass

import numpy as np
from scipy import ndimage
from skimage import color as skcolor
from skimage import filters

from . import color
from .metrics import island_mask

EDGE_PERCENTILE = 80   # cells above this percentile of edge strength take the edge rule
EDGE_FLOOR = 0.01      # ...but only when their Sobel strength is at least this
NEIGHBOURHOOD = 3      # cells; window used to decide darker side vs lighter side


@dataclass
class EdgeAwareResult:
    indices: np.ndarray        # (rows, cols) 0-based crayon indices
    edge_mask: np.ndarray      # cells colored by the edge rule
    smoothed_mask: np.ndarray  # cells changed by the island pass

    @property
    def n_edge_cells(self):
        return int(self.edge_mask.sum())

    @property
    def n_smoothed(self):
        return int(self.smoothed_mask.sum())


def cell_blocks(array, cols, rows):
    """(rows*S, cols*S, C) -> (rows, cols, S*S, C)."""
    s = array.shape[0] // rows
    c = array.shape[2]
    blocks = array.reshape(rows, s, cols, s, c).transpose(0, 2, 1, 3, 4)
    return blocks.reshape(rows, cols, s * s, c)


def luminance(rgb_uint8):
    return skcolor.rgb2gray(np.asarray(rgb_uint8, dtype=np.float64) / 255.0)


def edge_strength(gray, cols, rows):
    """Mean Sobel magnitude of the luminance copy within each cell."""
    sobel = filters.sobel(gray)
    return cell_blocks(sobel[..., None], cols, rows).mean(axis=(2, 3))


def edge_cell_mask(strength):
    threshold = max(np.percentile(strength, EDGE_PERCENTILE), EDGE_FLOOR)
    return strength >= threshold


def flat_cell_colors(lab_blocks):
    """Mean Lab of each block, snapped to the nearest crayon."""
    return color.nearest_palette(lab_blocks.mean(axis=2))


def edge_cell_colors(lab_blocks, lum_blocks, mask):
    """For masked cells: dominant crayon of the darker or lighter side.

    The block is split at its own mean luminance. A cell that is darker than
    its neighbourhood takes the dark side (keeps thin dark outlines); any other
    cell takes the light side (keeps highlights and the bright side of a border).
    Returns an (rows, cols) array; unmasked cells are -1.
    """
    rows, cols = mask.shape
    out = np.full((rows, cols), -1, dtype=int)
    cell_lum = lum_blocks.mean(axis=2)
    neighbourhood = ndimage.uniform_filter(cell_lum, size=NEIGHBOURHOOD, mode="nearest")
    for r, c in zip(*np.nonzero(mask)):
        lum = lum_blocks[r, c]  # (S*S,)
        dark = lum <= lum.mean()
        side = dark if cell_lum[r, c] < neighbourhood[r, c] else ~dark
        if not side.any():  # perfectly flat block: use every pixel
            side = np.ones_like(dark)
        pixel_idx = color.nearest_palette(lab_blocks[r, c][side])
        out[r, c] = np.bincount(pixel_idx, minlength=len(color.PALETTE_LAB)).argmax()
    return out


def remove_islands(indices, edge_mask, cell_lab):
    """Recolor single-cell islands unless the cell itself is an edge cell.

    An island has no 4-neighbour with the same crayon. It takes the most common
    neighbour crayon; ties go to the neighbour crayon nearest its own mean Lab.
    """
    rows, cols = indices.shape
    result = indices.copy()
    changed = np.zeros_like(edge_mask)
    candidates = island_mask(indices) & ~edge_mask
    for r, c in zip(*np.nonzero(candidates)):
        neighbours = [indices[rr, cc]
                      for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
                      if 0 <= rr < rows and 0 <= cc < cols]
        counts = np.bincount(neighbours, minlength=len(color.PALETTE_LAB))
        best = np.flatnonzero(counts == counts.max())
        if len(best) > 1:
            dist = ((color.PALETTE_LAB[best] - cell_lab[r, c]) ** 2).sum(axis=1)
            best = best[[dist.argmin()]]
        result[r, c] = best[0]
        changed[r, c] = True
    return result, changed


def color_cells(work_rgb, cols, rows):
    """Run the whole method on a (rows*S, cols*S, 3) uint8 image."""
    lab = color.rgb_to_lab(work_rgb)
    lab_blocks = cell_blocks(lab, cols, rows)
    gray = luminance(work_rgb)
    lum_blocks = cell_blocks(gray[..., None], cols, rows)[..., 0]

    strength = edge_strength(gray, cols, rows)
    mask = edge_cell_mask(strength)

    indices = flat_cell_colors(lab_blocks)
    edge_colors = edge_cell_colors(lab_blocks, lum_blocks, mask)
    indices = np.where(mask, edge_colors, indices)

    indices, smoothed = remove_islands(indices, mask, lab_blocks.mean(axis=2))
    return EdgeAwareResult(indices=indices, edge_mask=mask, smoothed_mask=smoothed)
