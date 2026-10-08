"""Run the edge-aware method for every loaded image and density."""

import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import config, edge_aware, inputs, metrics, render


@dataclass
class Record:
    loaded: inputs.LoadedImage
    cols: int
    rows: int
    result: edge_aware.EdgeAwareResult
    runtime: float
    fid: metrics.Fidelity
    recognizable: bool
    reason: str
    blank: object        # PIL image, kept for the geometry check
    tile: object         # side-by-side PIL image, kept for the contact sheet
    files: dict          # label -> path relative to docs/

    @property
    def indices(self):
        return self.result.indices

    @property
    def density(self):
        return f"{self.cols}x{self.rows}"


def process(loaded, cols, rows, out_dir=None, docs_dir=None):
    out_dir = Path(out_dir or config.OUT_DIR)
    docs_dir = Path(docs_dir or config.DOCS_DIR)
    cropped, _ = inputs.center_crop_3x4(loaded.image)

    start = time.perf_counter()
    work = np.asarray(inputs.resize_to_grid(cropped, cols, rows))
    result = edge_aware.color_cells(work, cols, rows)
    runtime = time.perf_counter() - start

    reference = edge_aware.cell_blocks(work, cols, rows).mean(axis=2).round().astype(np.uint8)
    fid = metrics.fidelity(result.indices, reference)
    ok, reason = metrics.recognizability(fid, metrics.distinct_crayons(result.indices))

    original = render.original_image(cropped, cols, rows)
    preview = render.preview_image(result.indices)
    blank = render.blank_grid_image(result.indices)
    tile = render.side_by_side(original, preview)

    folder = out_dir / loaded.spec.stem
    folder.mkdir(parents=True, exist_ok=True)
    density = f"{cols}x{rows}"
    paths = {"original": folder / f"original-{density}.png",
             "preview": folder / f"preview-{density}.png",
             "blank": folder / f"blank-{density}.png",
             "compare": folder / f"compare-{density}.png"}
    original.save(paths["original"])
    preview.save(paths["preview"])
    blank.save(paths["blank"])
    tile.save(paths["compare"])
    files = {k: p.relative_to(docs_dir).as_posix() for k, p in paths.items()}
    return Record(loaded, cols, rows, result, runtime, fid, ok, reason, blank, tile, files)


def run_all(images, out_dir=None, docs_dir=None):
    """Returns {density: [Record, ...]} in pinned image order (missing images skipped)."""
    records = {d: [] for d in config.DENSITIES}
    for loaded in images:
        if loaded.missing:
            continue
        for cols, rows in config.DENSITIES:
            records[(cols, rows)].append(process(loaded, cols, rows, out_dir, docs_dir))
    return records


def write_contact_sheets(records, out_dir=None, docs_dir=None):
    out_dir = Path(out_dir or config.OUT_DIR)
    docs_dir = Path(docs_dir or config.DOCS_DIR)
    paths = {}
    for (cols, rows), recs in records.items():
        if not recs:
            continue
        sheet = render.contact_sheet([r.tile for r in recs], [r.loaded.spec.stem for r in recs])
        path = out_dir / f"contact-sheet-{cols}x{rows}.png"
        sheet.save(path)
        paths[(cols, rows)] = path.relative_to(docs_dir).as_posix()
    return paths
