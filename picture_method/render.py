"""Rendering shared by every method: colored previews, blank numbered grids, contact sheets."""

import hashlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .palette import PALETTE_RGB

PREVIEW_CELL_PX = {24: 20, 36: 14, 48: 10}
BLANK_CELL_PX = {24: 40, 36: 32, 48: 28}
TILE_CELL_PX = {24: 8, 36: 6, 48: 5}
GRID_GRAY = 170  # every blank grid uses the same line gray and a white cell fill
MARGIN = 12


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow: no scalable default font
        return ImageFont.load_default()


def render_preview(indices, cell_px):
    """Flat crayon-colored cells, no lines and no numbers."""
    colors = PALETTE_RGB[indices].astype(np.uint8)
    colors = np.repeat(np.repeat(colors, cell_px, axis=0), cell_px, axis=1)
    return Image.fromarray(colors)


def render_blank(indices, cell_px, show_numbers=True):
    """Blank worksheet: uniform white cells, thin uniform grid lines, 1-24 numbers only.

    With show_numbers=False only the cell geometry is drawn, which is what the
    privacy check compares between pictures. Grayscale mode: no colors at all.
    """
    rows, cols = indices.shape
    image = Image.new("L", (cols * cell_px + 1, rows * cell_px + 1), 255)
    draw = ImageDraw.Draw(image)
    for c in range(cols + 1):
        draw.line([(c * cell_px, 0), (c * cell_px, rows * cell_px)], fill=GRID_GRAY)
    for r in range(rows + 1):
        draw.line([(0, r * cell_px), (cols * cell_px, r * cell_px)], fill=GRID_GRAY)
    if show_numbers:
        font = _font(int(cell_px * 0.5))
        for r in range(rows):
            for c in range(cols):
                draw.text(
                    (c * cell_px + cell_px / 2, r * cell_px + cell_px / 2),
                    str(int(indices[r, c]) + 1), fill=0, font=font, anchor="mm",
                )
    return image


def geometry_signature(indices, cell_px):
    """Hash of the number-free blank grid; equal hashes mean identical cell geometry."""
    image = render_blank(indices, cell_px, show_numbers=False)
    return hashlib.sha256(image.tobytes()).hexdigest(), sorted(set(image.getdata()))


def side_by_side(original, preview):
    """Original (resized to the preview's size) on the left, colored preview on the right."""
    original = original.resize(preview.size, Image.LANCZOS)
    sheet = Image.new("RGB", (preview.width * 2 + MARGIN, preview.height), "white")
    sheet.paste(original, (0, 0))
    sheet.paste(preview, (preview.width + MARGIN, 0))
    return sheet


def contact_sheet(entries, density, columns=3):
    """All 11 pinned images for one density, in pinned order.

    entries: list of (label, original cropped PIL image or None, indices or None, note).
    Missing images get a placeholder tile saying MISSING.
    """
    cols, rows = density
    cell_px = TILE_CELL_PX[cols]
    tile_w, tile_h = cols * cell_px, rows * cell_px
    label_h = 20
    cell_w = tile_w * 2 + MARGIN
    n_rows = -(-len(entries) // columns)
    sheet = Image.new("RGB", (columns * (cell_w + MARGIN) + MARGIN,
                              n_rows * (tile_h + label_h + MARGIN) + MARGIN), "white")
    draw = ImageDraw.Draw(sheet)
    font = _font(13)
    for i, (label, original, indices, note) in enumerate(entries):
        x = MARGIN + (i % columns) * (cell_w + MARGIN)
        y = MARGIN + (i // columns) * (tile_h + label_h + MARGIN)
        draw.text((x, y), label, fill=0, font=font)
        y += label_h
        if indices is None:
            draw.rectangle([x, y, x + cell_w, y + tile_h], outline=(150, 150, 150))
            draw.text((x + cell_w / 2, y + tile_h / 2), f"MISSING\n{note}"[:60], fill=(180, 0, 0),
                      font=font, anchor="mm", align="center")
            continue
        preview = render_preview(indices, cell_px)
        sheet.paste(original.resize(preview.size, Image.LANCZOS), (x, y))
        sheet.paste(preview, (x + tile_w + MARGIN, y))
    return sheet
