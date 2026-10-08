"""Palette handling: RGB <-> Lab and snapping to the nearest crayon."""

import numpy as np
from skimage import color as skcolor

from . import config


def hex_to_rgb(hex_value):
    return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))


PALETTE_NAMES = [name for name, _ in config.PALETTE]
PALETTE_RGB = np.array([hex_to_rgb(h) for _, h in config.PALETTE], dtype=np.uint8)


def rgb_to_lab(rgb_uint8):
    """Convert an (..., 3) uint8 RGB array to float Lab."""
    return skcolor.rgb2lab(np.asarray(rgb_uint8, dtype=np.float64) / 255.0)


PALETTE_LAB = rgb_to_lab(PALETTE_RGB.reshape(1, -1, 3)).reshape(-1, 3)


def nearest_palette(lab):
    """Index (0-based) of the nearest crayon in Lab (CIE76) for each (..., 3) color."""
    flat = np.asarray(lab, dtype=np.float64).reshape(-1, 3)
    dist = ((flat[:, None, :] - PALETTE_LAB[None, :, :]) ** 2).sum(axis=2)
    return dist.argmin(axis=1).reshape(np.shape(lab)[:-1])
