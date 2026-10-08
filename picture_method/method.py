"""Method: quantize then majority vote.

Three separate steps, each a function:
  1. downscale_to_subpixels: resize the cropped image to (cols*S, rows*S) pixels,
     so each grid cell covers an S x S block of pixels.
  2. quantize_pixels: map EVERY pixel to its nearest crayon in Lab space
     (optionally with Floyd-Steinberg error diffusion).
  3. vote_cells: each cell takes the crayon most common among its S*S pixels;
     ties go to the tied crayon with the larger share in the 8 neighboring cells.
"""

import time
from dataclasses import dataclass

import numpy as np
from PIL import Image

from .palette import palette_lab, rgb_to_lab

SUBPIXELS = 6  # S: pixels per cell side before voting


@dataclass
class GridResult:
    grid: np.ndarray  # (rows, cols) crayon index 0..23; printed number = index + 1
    cell_mean_lab: np.ndarray  # (rows, cols, 3) mean Lab of the ORIGINAL pixels in each cell
    tie_cells: int  # cells whose vote needed the neighbor tie-break
    seconds: float  # downscale + quantize + vote, excluding image decoding


def downscale_to_subpixels(img, cols, rows, subpixels=SUBPIXELS):
    """Step 1: whole-image downscale to S pixels per cell side (Lanczos)."""
    return np.asarray(img.resize((cols * subpixels, rows * subpixels), Image.LANCZOS))


def quantize_pixels(rgb, pal_lab, dither=False):
    """Step 2: nearest crayon (Euclidean distance in Lab) for every pixel -> (H, W) labels."""
    lab = rgb_to_lab(rgb)
    if dither:
        return _floyd_steinberg(lab, pal_lab)
    dist = ((lab[:, :, None, :] - pal_lab[None, None, :, :]) ** 2).sum(axis=-1)
    return dist.argmin(axis=-1)


def _floyd_steinberg(lab, pal_lab):
    """Floyd-Steinberg error diffusion in Lab, left to right, top to bottom."""
    h, w, _ = lab.shape
    work = lab.copy()
    out = np.empty((h, w), dtype=np.int64)
    lo = np.array([0.0, -128.0, -128.0])
    hi = np.array([100.0, 127.0, 127.0])
    for y in range(h):
        for x in range(w):
            px = np.clip(work[y, x], lo, hi)
            k = int(((pal_lab - px) ** 2).sum(axis=1).argmin())
            out[y, x] = k
            err = px - pal_lab[k]
            if x + 1 < w:
                work[y, x + 1] += err * (7 / 16)
            if y + 1 < h:
                if x > 0:
                    work[y + 1, x - 1] += err * (3 / 16)
                work[y + 1, x] += err * (5 / 16)
                if x + 1 < w:
                    work[y + 1, x + 1] += err * (1 / 16)
    return out


def count_votes(labels, cols, rows, subpixels=SUBPIXELS, n_colors=24):
    """Per-cell histogram of crayon labels -> (rows, cols, n_colors) counts."""
    blocks = labels.reshape(rows, subpixels, cols, subpixels).transpose(0, 2, 1, 3)
    blocks = blocks.reshape(rows, cols, subpixels * subpixels)
    counts = np.zeros((rows, cols, n_colors), dtype=np.int64)
    for k in range(n_colors):
        counts[:, :, k] = (blocks == k).sum(axis=-1)
    return counts


def neighbor_counts(counts):
    """Sum of the histograms of the (up to) 8 surrounding cells."""
    rows, cols, _ = counts.shape
    padded = np.pad(counts, ((1, 1), (1, 1), (0, 0)))
    total = np.zeros_like(counts)
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            if (dy, dx) != (1, 1):
                total += padded[dy : dy + rows, dx : dx + cols]
    return total


def vote_cells(counts):
    """Step 3: majority crayon per cell; ties -> larger neighboring share, then lowest index."""
    top = counts.max(axis=-1, keepdims=True)
    tied = counts == top
    needs_tiebreak = tied.sum(axis=-1) > 1
    neighbors = neighbor_counts(counts)
    # argmax returns the first maximum, i.e. the lowest crayon index on a remaining tie
    grid = np.where(tied, neighbors, -1).argmax(axis=-1)
    return grid, int(needs_tiebreak.sum())


def quantize_then_vote(img, cols, rows, dither=False, subpixels=SUBPIXELS):
    """Run the whole method on a 3:4-cropped PIL image."""
    pal_lab = palette_lab()
    start = time.perf_counter()
    rgb = downscale_to_subpixels(img, cols, rows, subpixels)
    labels = quantize_pixels(rgb, pal_lab, dither=dither)
    counts = count_votes(labels, cols, rows, subpixels, len(pal_lab))
    grid, ties = vote_cells(counts)
    seconds = time.perf_counter() - start
    lab = rgb_to_lab(rgb)
    cell_lab = lab.reshape(rows, subpixels, cols, subpixels, 3).mean(axis=(1, 3))
    return GridResult(grid=grid, cell_mean_lab=cell_lab, tie_cells=ties, seconds=seconds)
