"""Regenerates everything for the 'quantize then majority vote' method.

Usage: python run_picture_method.py
Writes photos/, docs/picture-method-results.md and docs/picture-method/quantize-vote/,
and prints the report.
"""

import os
import sys

from picture_method import inputs, metrics, render
from picture_method.method import SUBPIXELS, quantize_then_vote
from picture_method.report import build_report

DENSITIES = [(24, 32), (36, 48), (48, 64)]  # columns x rows
PREVIEW_CELL_PX = {(24, 32): 20, (36, 48): 15, (48, 64): 10}
ORIGINAL_SIZE = (360, 480)
PHOTO_DIR = "photos"
DOCS_DIR = "docs"
REPORT_PATH = os.path.join(DOCS_DIR, "picture-method-results.md")
METHOD_NAME = "quantize-vote"
METHOD_DIR = os.path.join(DOCS_DIR, "picture-method", METHOD_NAME)
DITHER_DIR = os.path.join(METHOD_DIR, "dither")


def rel(path):
    """Path as seen from the report file's directory."""
    return os.path.relpath(path, DOCS_DIR)


def process_image(item, cropped, density, files_dir):
    cols, rows = density
    tag = f"{item.spec.number:02d}-{item.spec.name}_{cols}x{rows}"
    plain = quantize_then_vote(cropped, cols, rows, dither=False)
    dithered = quantize_then_vote(cropped, cols, rows, dither=True)

    preview = render.render_preview(plain.grid, PREVIEW_CELL_PX[density])
    blank = render.render_blank(plain.grid)
    files = {
        "original": os.path.join(files_dir, f"{item.spec.number:02d}-{item.spec.name}_original.png"),
        "preview": os.path.join(files_dir, f"{tag}_preview.png"),
        "blank": os.path.join(files_dir, f"{tag}_blank.png"),
    }
    files["blank_rel"] = files["blank"]
    preview.save(files["preview"])
    blank.save(files["blank"])

    plain_m = metrics.grid_metrics(plain)
    plain_m["grid"] = plain.grid
    dither_m = metrics.grid_metrics(dithered)
    dither_m["grid"] = dithered.grid
    record = {
        "item": item,
        "density": density,
        "files": files,
        "plain": plain_m,
        "dither": dither_m,
        "recog": metrics.recognizability(plain_m),
        "blank_ok": render.check_blank(blank, rows, cols),
    }
    return record, preview, render.render_preview(dithered.grid, PREVIEW_CELL_PX[density])


def main():
    os.makedirs(METHOD_DIR, exist_ok=True)
    os.makedirs(DITHER_DIR, exist_ok=True)
    sources = inputs.fetch_all(PHOTO_DIR)
    ok = [s for s in sources if s.status == "OK"]
    for s in sources:
        print(f"{s.spec.filename}: {s.status} {s.reason}", file=sys.stderr)
    if not ok:
        print("No pinned image could be read; nothing to report.", file=sys.stderr)
        return 1

    records = []
    sheets = {d: {"plain": {}, "dither": {}} for d in DENSITIES}
    for item in ok:
        cropped = inputs.load_cropped(item)
        render.render_original(cropped, ORIGINAL_SIZE).save(
            os.path.join(METHOD_DIR, f"{item.spec.number:02d}-{item.spec.name}_original.png")
        )
        for density in DENSITIES:
            record, preview, dither_preview = process_image(item, cropped, density, METHOD_DIR)
            records.append(record)
            sheets[density]["plain"][item.spec.number] = preview
            sheets[density]["dither"][item.spec.number] = dither_preview
            print(f"done {item.spec.filename} {density[0]}x{density[1]}", file=sys.stderr)

    sheet_files = {}
    for density in DENSITIES:
        for variant, folder in (("plain", METHOD_DIR), ("dither", DITHER_DIR)):
            entries = [
                (s.spec.filename, sheets[density][variant].get(s.spec.number)) for s in sources
            ]
            path = os.path.join(folder, f"contact_{density[0]}x{density[1]}.png")
            render.contact_sheet(entries).save(path)
            if variant == "plain":
                sheet_files[density] = path

    blank_checks = {
        d: (sum(r["blank_ok"] for r in records if r["density"] == d), sum(1 for r in records if r["density"] == d))
        for d in DENSITIES
    }
    first = DENSITIES[0]
    first_recs = [r for r in records if r["density"] == first]
    examples = first_recs[:3]

    text = build_report(
        sources, records, DENSITIES, METHOD_DIR, {"subpixels": SUBPIXELS}, sheet_files, blank_checks, examples, rel
    )
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
