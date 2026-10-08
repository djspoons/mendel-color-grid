"""Metrics on a finished grid (rows, cols) of crayon indexes."""

import numpy as np

from .palette import palette_lab


def usage(grid, n_colors=24):
    return np.bincount(grid.ravel(), minlength=n_colors)


def distinct_crayons(grid):
    return int((usage(grid) > 0).sum())


def top3_share(grid):
    return float(np.sort(usage(grid))[-3:].sum() / grid.size)


def same_adjacent_share(grid):
    """Share of 4-neighbor adjacent cell pairs that carry the same number."""
    horiz = grid[:, 1:] == grid[:, :-1]
    vert = grid[1:, :] == grid[:-1, :]
    return float((horiz.sum() + vert.sum()) / (horiz.size + vert.size))


def chance_same_adjacent(grid):
    """Expected same-number share if the same numbers were scattered at random."""
    p = usage(grid) / grid.size
    return float((p**2).sum())


def island_count(grid):
    """Cells whose every existing 4-neighbor has a different number."""
    same = np.zeros(grid.shape, dtype=bool)
    same[:, 1:] |= grid[:, 1:] == grid[:, :-1]
    same[:, :-1] |= grid[:, :-1] == grid[:, 1:]
    same[1:, :] |= grid[1:, :] == grid[:-1, :]
    same[:-1, :] |= grid[:-1, :] == grid[1:, :]
    return int((~same).sum())


def mean_run_length(grid):
    """Average length of runs of equal numbers along rows."""
    changes = (grid[:, 1:] != grid[:, :-1]).sum()
    runs = grid.shape[0] + changes
    return float(grid.size / runs)


def fidelity(grid, cell_mean_lab):
    """(mean Lab distance to the original's cell colors, lightness correlation)."""
    chosen = palette_lab()[grid]
    delta_e = float(np.sqrt(((chosen - cell_mean_lab) ** 2).sum(axis=-1)).mean())
    a, b = chosen[..., 0].ravel(), cell_mean_lab[..., 0].ravel()
    if a.std() < 1e-9 or b.std() < 1e-9:
        return delta_e, 0.0
    return delta_e, float(np.corrcoef(a, b)[0, 1])


def grid_metrics(result):
    grid = result.grid
    delta_e, corr = fidelity(grid, result.cell_mean_lab)
    return {
        "distinct": distinct_crayons(grid),
        "top3": top3_share(grid),
        "same_adjacent": same_adjacent_share(grid),
        "chance_adjacent": chance_same_adjacent(grid),
        "islands": island_count(grid),
        "island_share": island_count(grid) / grid.size,
        "run_length": mean_run_length(grid),
        "delta_e": delta_e,
        "lightness_corr": corr,
        "tie_cells": result.tie_cells,
        "seconds": result.seconds,
    }


def recognizability(m):
    """Computed proxy for 'is the preview recognizable' -> (verdict, reasons).

    Thresholds are heuristics on lightness correlation with the original and on
    speckle; they stand in for an eyeball judgement, which this script cannot make.
    """
    reasons = []
    if m["lightness_corr"] < 0.85:
        reasons.append(f"light/dark structure only partly kept (lightness r={m['lightness_corr']:.2f})")
    if m["island_share"] > 0.08:
        reasons.append(f"speckled ({m['island_share'] * 100:.0f}% of cells are single-cell islands)")
    if m["distinct"] <= 5:
        reasons.append(f"only {m['distinct']} crayons survive the vote")
    if m["top3"] > 0.85:
        reasons.append(f"top 3 crayons fill {m['top3'] * 100:.0f}% of cells (detail lost)")
    if m["lightness_corr"] >= 0.85 and not reasons:
        return "recognizable", []
    if m["lightness_corr"] >= 0.7:
        return "partly recognizable", reasons
    return "not recognizable", reasons
