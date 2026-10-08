"""Rendering: colored previews, blank numbered grids, contact sheets."""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .palette import palette_rgb

BLANK_CELL_PX = 28  # same for every density and every image
BLANK_MARGIN_PX = 2  # ring inside each cell that must stay pure white
SHEET_THUMB = (240, 320)


def render_preview(grid, cell_px):
    rgb = palette_rgb()[grid]
    img = Image.fromarray(rgb, "RGB")
    return img.resize((grid.shape[1] * cell_px, grid.shape[0] * cell_px), Image.NEAREST)


def render_blank(grid, cell_px=BLANK_CELL_PX):
    """Uniform cells on white; only the cell's palette number is drawn (black, 1-24)."""
    rows, cols = grid.shape
    img = Image.new("L", (cols * cell_px, rows * cell_px), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=int(cell_px * 0.5))
    for y in range(rows):
        for x in range(cols):
            center = (x * cell_px + cell_px / 2, y * cell_px + cell_px / 2)
            draw.text(center, str(int(grid[y, x]) + 1), fill=0, font=font, anchor="mm")
    return img


def check_blank(img, rows, cols, cell_px=BLANK_CELL_PX):
    """Verify the blank sheet: right size, grayscale, and no ink on any cell's edge ring.

    A white ring in every cell means there are no outlines, grid lines or shading
    (fills) at cell boundaries, so geometry is the same uniform lattice for any image.
    """
    if img.mode != "L" or img.size != (cols * cell_px, rows * cell_px):
        return False
    a = np.asarray(img)
    cells = a.reshape(rows, cell_px, cols, cell_px).transpose(0, 2, 1, 3)
    m = BLANK_MARGIN_PX
    ring = np.ones((cell_px, cell_px), dtype=bool)
    ring[m:-m, m:-m] = False
    return bool((cells[:, :, ring] == 255).all())


def render_original(img, size):
    return img.resize(size, Image.LANCZOS)


def contact_sheet(entries, size=SHEET_THUMB, columns=4, pad=8, label_h=18):
    """entries: [(label, PIL image or None)] in pinned order; None draws a MISSING tile."""
    n = len(entries)
    rows = -(-n // columns)
    tw, th = size
    sheet = Image.new("RGB", (columns * (tw + pad) + pad, rows * (th + label_h + pad) + pad), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=12)
    for i, (label, img) in enumerate(entries):
        x = pad + (i % columns) * (tw + pad)
        y = pad + (i // columns) * (th + label_h + pad)
        draw.text((x, y), label, fill=(0, 0, 0), font=font)
        if img is None:
            draw.rectangle([x, y + label_h, x + tw - 1, y + label_h + th - 1], outline=(200, 0, 0))
            draw.text((x + tw // 2, y + label_h + th // 2), "MISSING", fill=(200, 0, 0), font=font, anchor="mm")
        else:
            sheet.paste(img.resize(size, Image.NEAREST), (x, y + label_h))
    return sheet
