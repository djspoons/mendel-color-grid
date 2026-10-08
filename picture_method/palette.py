"""The Crayola 24-count box and sRGB -> CIE Lab conversion (D65)."""

import numpy as np

# (name, hex). Cell numbers are the 1-based position in this list.
# Hex values are the ones Crayola publishes for these crayon names (as listed
# on Wikipedia's "List of Crayola crayon colors"); they are not measured.
CRAYONS = [
    ("Red", "#EE204D"),
    ("Yellow", "#FCE883"),
    ("Blue", "#1F75FE"),
    ("Brown", "#B5674D"),
    ("Orange", "#FF7538"),
    ("Green", "#1CAC78"),
    ("Violet", "#926EAE"),
    ("Black", "#232323"),
    ("Carnation Pink", "#FFAACC"),
    ("Yellow Green", "#C5E384"),
    ("Blue Green", "#0D98BA"),
    ("Red Orange", "#FF5349"),
    ("Red Violet", "#C0448F"),
    ("White", "#EDEDED"),
    ("Gray", "#95918C"),
    ("Yellow Orange", "#FFAE42"),
    ("Blue Violet", "#7366BD"),
    ("Apricot", "#FDD9B5"),
    ("Scarlet", "#FC2847"),
    ("Tan", "#FAA76C"),
    ("Sky Blue", "#80DAEB"),
    ("Peach", "#FFCBA4"),
    ("Orchid", "#E6A8D7"),
    ("Burnt Sienna", "#EA7E5D"),
]

_WHITE_D65 = np.array([0.95047, 1.0, 1.08883])
_RGB_TO_XYZ = np.array(
    [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ]
)


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def palette_rgb():
    """(24, 3) uint8 array of the crayon colors."""
    return np.array([hex_to_rgb(h) for _, h in CRAYONS], dtype=np.uint8)


def rgb_to_lab(rgb):
    """Convert sRGB uint8 values of shape (..., 3) to float CIE Lab."""
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    linear = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = linear @ _RGB_TO_XYZ.T / _WHITE_D65
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack(
        [116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])],
        axis=-1,
    )


def palette_lab():
    return rgb_to_lab(palette_rgb())
