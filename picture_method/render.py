"""Rendering: colored previews, blank numbered grids, comparisons, contact sheets."""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import color, config

LINE_GREY = (170, 170, 170)
TEXT_GREY = (40, 40, 40)
BACKGROUND = (255, 255, 255)


def cell_px(cols):
    return config.PREVIEW_WIDTH // cols


def preview_image(indices):
    """Colored preview: every cell painted with its crayon, uniform cell size."""
    rows, cols = indices.shape
    px = cell_px(cols)
    small = Image.fromarray(color.PALETTE_RGB[indices])
    return small.resize((cols * px, rows * px), Image.NEAREST)


def grid_line_mask(cols, rows):
    """Boolean mask of the pixels that are grid lines. Depends only on the density."""
    px = cell_px(cols)
    mask = np.zeros((rows * px, cols * px), dtype=bool)
    mask[::px, :] = True
    mask[:, ::px] = True
    mask[-1, :] = True
    mask[:, -1] = True
    return mask


def _font(px):
    size = max(7, int(px * 0.55))
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # old Pillow: fixed-size bitmap font
        return ImageFont.load_default()


def blank_grid_image(indices):
    """Numbers only: white cells, uniform thin grey grid lines, no colors, no outlines."""
    rows, cols = indices.shape
    px = cell_px(cols)
    img = Image.new("RGB", (cols * px, rows * px), BACKGROUND)
    draw = ImageDraw.Draw(img)
    font = _font(px)
    for r in range(rows):
        for c in range(cols):
            draw.text((c * px + px / 2, r * px + px / 2), str(int(indices[r, c]) + 1),
                      fill=TEXT_GREY, font=font, anchor="mm")
    arr = np.array(img)
    arr[grid_line_mask(cols, rows)] = LINE_GREY
    return Image.fromarray(arr)


def check_blank_geometry(blank_images, cols, rows):
    """Verify every blank grid has the same size and grid lines, and no color.

    Returns (ok, message).
    """
    expected = grid_line_mask(cols, rows)
    for i, img in enumerate(blank_images):
        arr = np.array(img)
        if arr.shape[:2] != expected.shape:
            return False, f"image {i} has size {arr.shape[:2]}, expected {expected.shape}"
        if not (arr[..., 0] == arr[..., 1]).all() or not (arr[..., 1] == arr[..., 2]).all():
            return False, f"image {i} contains colored pixels"
        if not (arr[expected] == LINE_GREY).all():
            return False, f"image {i} has grid lines that differ from the standard geometry"
    return True, (f"{len(blank_images)} blank grids: {expected.shape[1]}x{expected.shape[0]} px, "
                  f"cell {cell_px(cols)} px, identical grid lines, grayscale only")


def original_image(cropped, cols, rows):
    px = cell_px(cols)
    return cropped.resize((cols * px, rows * px), Image.LANCZOS)


def side_by_side(original, preview, gap=12):
    w, h = original.size
    canvas = Image.new("RGB", (w * 2 + gap, h), BACKGROUND)
    canvas.paste(original, (0, 0))
    canvas.paste(preview, (w + gap, 0))
    return canvas


def contact_sheet(tiles, labels, columns=3, tile_width=384, label_height=22):
    """tiles: side-by-side images (original | preview), laid out in the pinned order."""
    tile_height = round(tiles[0].height * tile_width / tiles[0].width)
    rows = -(-len(tiles) // columns)
    pad = 8
    sheet = Image.new("RGB", (columns * (tile_width + pad) + pad,
                              rows * (tile_height + label_height + pad) + pad), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = _font(28)
    for i, (tile, label) in enumerate(zip(tiles, labels)):
        x = pad + (i % columns) * (tile_width + pad)
        y = pad + (i // columns) * (tile_height + label_height + pad)
        draw.text((x, y + 2), label, fill=TEXT_GREY, font=font)
        sheet.paste(tile.resize((tile_width, tile_height), Image.LANCZOS), (x, y + label_height))
    return sheet
