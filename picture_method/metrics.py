"""Method-independent metrics over a grid of 0-based crayon indices."""

from dataclasses import dataclass

import numpy as np
from skimage import color as skcolor
from skimage import filters
from skimage.metrics import structural_similarity

from . import color, config

# Heuristic thresholds for the automated recognizability proxy.
SSIM_MIN = 0.45
EDGE_CORR_MIN = 0.45
MIN_CRAYONS = 5


def _neighbour_same(indices):
    """Boolean (rows, cols, 4) array: does the neighbour (up, down, left, right) match?
    Out-of-bounds neighbours are reported in the second array as invalid."""
    rows, cols = indices.shape
    same = np.zeros((rows, cols, 4), dtype=bool)
    valid = np.zeros((rows, cols, 4), dtype=bool)
    same[1:, :, 0] = indices[1:] == indices[:-1]
    valid[1:, :, 0] = True
    same[:-1, :, 1] = indices[:-1] == indices[1:]
    valid[:-1, :, 1] = True
    same[:, 1:, 2] = indices[:, 1:] == indices[:, :-1]
    valid[:, 1:, 2] = True
    same[:, :-1, 3] = indices[:, :-1] == indices[:, 1:]
    valid[:, :-1, 3] = True
    return same, valid


def island_mask(indices):
    """Cells with no 4-neighbour of the same crayon (single cell inside another color)."""
    same, valid = _neighbour_same(indices)
    return ~same.any(axis=2) & valid.any(axis=2)


def count_islands(indices):
    return int(island_mask(indices).sum())


def adjacent_same_share(indices):
    """Share of horizontally/vertically adjacent cell pairs that carry the same number."""
    horizontal = indices[:, 1:] == indices[:, :-1]
    vertical = indices[1:] == indices[:-1]
    total = horizontal.size + vertical.size
    return float((horizontal.sum() + vertical.sum()) / total)


def chance_same_share(indices):
    """Same-number share expected if the same numbers were shuffled over the grid."""
    p = np.bincount(indices.ravel(), minlength=len(config.PALETTE)) / indices.size
    return float((p ** 2).sum())


def mean_run_length(indices):
    """Average length of maximal runs of equal numbers along rows."""
    runs = 0
    for row in indices:
        runs += 1 + int((row[1:] != row[:-1]).sum())
    return float(indices.size / runs)


def palette_counts(indices):
    return np.bincount(indices.ravel(), minlength=len(config.PALETTE))


def distinct_crayons(indices):
    return int((palette_counts(indices) > 0).sum())


def top3_share(indices):
    counts = np.sort(palette_counts(indices))[::-1]
    return float(counts[:3].sum() / indices.size)


@dataclass
class Fidelity:
    mean_delta_e: float
    luma_ssim: float
    edge_corr: float


def fidelity(indices, reference_rgb):
    """Compare the colored grid with the original's per-cell mean (a (rows, cols, 3) uint8).

    Used only as an automated proxy for 'recognizable'; it is not a human judgement.
    """
    painted = color.PALETTE_RGB[indices]
    delta = np.sqrt(((color.PALETTE_LAB[indices] - color.rgb_to_lab(reference_rgb)) ** 2).sum(axis=2))
    gray_p = _gray(painted)
    gray_r = _gray(reference_rgb)
    ssim = structural_similarity(gray_p, gray_r, data_range=1.0)
    edge_p = filters.sobel(gray_p).ravel()
    edge_r = filters.sobel(gray_r).ravel()
    corr = float(np.corrcoef(edge_p, edge_r)[0, 1]) if edge_p.std() > 0 and edge_r.std() > 0 else 0.0
    return Fidelity(float(delta.mean()), float(ssim), corr)


def _gray(rgb):
    return skcolor.rgb2gray(np.asarray(rgb, dtype=np.float64) / 255.0)


def recognizability(fid, n_crayons):
    """(is_recognizable, reason) from the proxy thresholds."""
    problems = []
    if fid.luma_ssim < SSIM_MIN:
        problems.append(f"light/dark structure differs from the original (luminance SSIM {fid.luma_ssim:.2f} < {SSIM_MIN})")
    if fid.edge_corr < EDGE_CORR_MIN:
        problems.append(f"outlines not retained (edge correlation {fid.edge_corr:.2f} < {EDGE_CORR_MIN})")
    if n_crayons < MIN_CRAYONS:
        problems.append(f"only {n_crayons} crayons used")
    return (not problems), "; ".join(problems)
