"""The classic Crayola 24-count box and the CIE Lab helpers used to match colors."""

import numpy as np

# (name, hex). Cell numbers are 1-based positions in this list.
CRAYONS = [
    ("Red", "#EE204D"),
    ("Yellow", "#FCE883"),
    ("Blue", "#1F75FE"),
    ("Brown", "#B4674D"),
    ("Orange", "#FF7538"),
    ("Green", "#1CAC78"),
    ("Violet", "#926EAE"),
    ("Black", "#000000"),
    ("Carnation Pink", "#FFAACC"),
    ("Yellow Green", "#C5E384"),
    ("Blue Green", "#0D98BA"),
    ("Red Orange", "#FF5349"),
    ("Red Violet", "#C0448F"),
    ("Yellow Orange", "#FFB653"),
    ("Blue Violet", "#7366BD"),
    ("White", "#FFFFFF"),
    ("Violet Red", "#F75394"),
    ("Dandelion", "#FDDB6D"),
    ("Cerulean", "#1DACD6"),
    ("Apricot", "#FDD9B5"),
    ("Scarlet", "#FC2847"),
    ("Green Yellow", "#F0E891"),
    ("Indigo", "#5D76CB"),
    ("Gray", "#95918C"),
]

_D65_WHITE = np.array([0.95047, 1.0, 1.08883])
_SRGB_TO_XYZ = np.array(
    [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ]
)


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def srgb_to_lab(rgb):
    """Convert sRGB values in 0..255, shape (..., 3), to CIE Lab (D65)."""
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    linear = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = (linear @ _SRGB_TO_XYZ.T) / _D65_WHITE
    delta = 6 / 29
    f = np.where(xyz > delta**3, np.cbrt(xyz), xyz / (3 * delta**2) + 4 / 29)
    lightness = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([lightness, a, b], axis=-1)


PALETTE_RGB = np.array([hex_to_rgb(h) for _, h in CRAYONS], dtype=np.float64)
PALETTE_LAB = srgb_to_lab(PALETTE_RGB)
