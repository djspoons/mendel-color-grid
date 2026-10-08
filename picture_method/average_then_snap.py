"""Method: average then snap.

1. (optional) mild contrast and saturation boost on the cropped picture
2. average each grid cell's pixels to one mean color
3. snap each mean to the nearest of the 24 crayons by distance in CIE Lab

Each step is its own function so it can be read, tested and ported separately.
"""

from dataclasses import dataclass

import numpy as np
from PIL import ImageEnhance

from .palette import PALETTE_LAB, srgb_to_lab
from .preprocess import cell_means


@dataclass(frozen=True)
class Boost:
    """Contrast and saturation factors applied before averaging (1.0 = unchanged)."""

    contrast: float = 1.10
    saturation: float = 1.15

    @property
    def enabled(self):
        return self.contrast != 1.0 or self.saturation != 1.0

    def describe(self):
        if not self.enabled:
            return "off"
        return f"on (contrast x{self.contrast:.2f}, saturation x{self.saturation:.2f})"


DEFAULT_BOOST = Boost()


def apply_boost(image, boost):
    """Step 1: contrast then saturation boost on a PIL image."""
    if not boost.enabled:
        return image
    image = ImageEnhance.Contrast(image).enhance(boost.contrast)
    return ImageEnhance.Color(image).enhance(boost.saturation)


def average_cells(image, cols, rows):
    """Step 2: mean color of each cell, shape (rows, cols, 3), sRGB 0..255."""
    return cell_means(np.asarray(image), cols, rows)


def snap_to_palette(means):
    """Step 3: index (0..23) of the nearest crayon for each mean, by Euclidean distance in Lab."""
    lab = srgb_to_lab(means)
    distances = np.linalg.norm(lab[..., None, :] - PALETTE_LAB, axis=-1)
    return distances.argmin(axis=-1)


def average_then_snap(cropped, cols, rows, boost=DEFAULT_BOOST):
    """Run the three steps on a 3:4-cropped PIL image; returns (rows, cols) crayon indices."""
    boosted = apply_boost(cropped, boost)
    means = average_cells(boosted, cols, rows)
    return snap_to_palette(means)
