"""Method-independent metrics, computed on a (rows, cols) grid of crayon indices."""

import numpy as np

from .palette import PALETTE_LAB, srgb_to_lab

N_CRAYONS = len(PALETTE_LAB)

# Automated recognizability proxy: thresholds are judgment calls, not human ratings.
MIN_LUMINANCE_CORR = 0.85
MIN_CRAYONS = 5
MAX_MEAN_DELTA_E = 30.0


def fidelity(reference_means, indices):
    """Compare the snapped grid with the original's plain cell means (no boost).

    Returns (luminance correlation in Lab L, mean Lab distance).
    """
    reference = srgb_to_lab(reference_means)
    snapped = PALETTE_LAB[indices]
    delta_e = float(np.linalg.norm(reference - snapped, axis=-1).mean())
    a, b = reference[..., 0].ravel(), snapped[..., 0].ravel()
    corr = 0.0 if a.std() == 0 or b.std() == 0 else float(np.corrcoef(a, b)[0, 1])
    return corr, delta_e


def recognizability(corr, delta_e, distinct):
    """Proxy verdict: (recognizable?, reasons it is not)."""
    reasons = []
    if corr < MIN_LUMINANCE_CORR:
        reasons.append(f"light/dark structure lost (L correlation {corr:.2f} < {MIN_LUMINANCE_CORR})")
    if distinct < MIN_CRAYONS:
        reasons.append(f"only {distinct} crayons used")
    if delta_e > MAX_MEAN_DELTA_E:
        reasons.append(f"colors far from the original (mean dE {delta_e:.1f} > {MAX_MEAN_DELTA_E:.0f})")
    return not reasons, reasons


def distinct_crayons(indices):
    return int(len(np.unique(indices)))


def top3_share(indices):
    counts = np.bincount(indices.ravel(), minlength=N_CRAYONS)
    return float(np.sort(counts)[-3:].sum() / indices.size)


def usage_counts(grids):
    """Total cells per crayon over a list of grids."""
    return sum(np.bincount(g.ravel(), minlength=N_CRAYONS) for g in grids)


def adjacent_same_share(indices):
    """Share of horizontally and vertically adjacent cell pairs holding the same number."""
    horizontal = indices[:, 1:] == indices[:, :-1]
    vertical = indices[1:, :] == indices[:-1, :]
    return float((horizontal.sum() + vertical.sum()) / (horizontal.size + vertical.size))


def shuffled_adjacent_share(indices, repeats=5, seed=0):
    """Same measure after randomly permuting the cells: what no spatial structure would give."""
    rng = np.random.default_rng(seed)
    shares = []
    for _ in range(repeats):
        flat = indices.ravel().copy()
        rng.shuffle(flat)
        shares.append(adjacent_same_share(flat.reshape(indices.shape)))
    return float(np.mean(shares))


def island_count(indices):
    """Cells whose every existing up/down/left/right neighbour has a different number."""
    padded = np.pad(indices, 1, constant_values=-1)
    same = (
        (padded[:-2, 1:-1] == indices)
        | (padded[2:, 1:-1] == indices)
        | (padded[1:-1, :-2] == indices)
        | (padded[1:-1, 2:] == indices)
    )
    return int((~same).sum())


def mean_row_run_length(indices):
    """Average length of runs of equal numbers along rows."""
    runs = indices.shape[0] + int((indices[:, 1:] != indices[:, :-1]).sum())
    return float(indices.size / runs)
