"""Run average-then-snap on every loaded image at every density and collect the numbers."""

import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import metrics, render
from .average_then_snap import DEFAULT_BOOST, average_then_snap
from .preprocess import DENSITIES, cell_means, center_crop_3x4

METHOD = "average-then-snap"
TIMING_REPEATS = 3


@dataclass
class Result:
    name: str
    category: str
    density: tuple
    indices: np.ndarray
    seconds: float
    distinct: int
    top3: float
    corr: float
    delta_e: float
    recognizable: bool
    reasons: list
    same_share: float
    shuffled_share: float
    islands: int
    run_length: float
    compare_file: str = ""
    blank_file: str = ""
    blank_geometry: str = ""
    blank_colors: list = field(default_factory=list)
    blank_is_gray: bool = True


def density_label(density):
    return f"{density[0]}x{density[1]}"


def analyze(name, category, cropped, density, boost):
    """Run the method on one cropped picture at one density and measure the result."""
    cols, rows = density
    timings = []
    for _ in range(TIMING_REPEATS):
        start = time.perf_counter()
        indices = average_then_snap(cropped, cols, rows, boost)
        timings.append(time.perf_counter() - start)
    reference = cell_means(np.asarray(cropped), cols, rows)  # original colors, no boost
    corr, delta_e = metrics.fidelity(reference, indices)
    distinct = metrics.distinct_crayons(indices)
    recognizable, reasons = metrics.recognizability(corr, delta_e, distinct)
    return Result(
        name=name, category=category, density=density, indices=indices,
        seconds=statistics.median(timings), distinct=distinct,
        top3=metrics.top3_share(indices), corr=corr, delta_e=delta_e,
        recognizable=recognizable, reasons=reasons,
        same_share=metrics.adjacent_same_share(indices),
        shuffled_share=metrics.shuffled_adjacent_share(indices),
        islands=metrics.island_count(indices),
        run_length=metrics.mean_row_run_length(indices),
    )


def write_images(result, cropped, out_dir, docs_dir):
    """Write the side-by-side preview and the blank numbered grid; record the blank-sheet checks."""
    cols = result.density[0]
    stem = f"{result.name}_{density_label(result.density)}"
    preview = render.render_preview(result.indices, render.PREVIEW_CELL_PX[cols])
    compare_path = Path(out_dir) / f"{stem}_compare.png"
    render.side_by_side(cropped, preview).save(compare_path)
    blank = render.render_blank(result.indices, render.BLANK_CELL_PX[cols])
    blank_path = Path(out_dir) / f"{stem}_blank.png"
    blank.save(blank_path)
    result.compare_file = compare_path.relative_to(docs_dir).as_posix()
    result.blank_file = blank_path.relative_to(docs_dir).as_posix()
    result.blank_geometry, result.blank_colors = render.geometry_signature(
        result.indices, render.BLANK_CELL_PX[cols])
    result.blank_is_gray = blank.mode == "L"


def run_all(loaded_images, docs_dir, boost=DEFAULT_BOOST):
    """Returns (results, crops, contact_sheet_paths). Missing images are skipped."""
    docs_dir = Path(docs_dir)
    out_dir = docs_dir / "picture-method" / METHOD
    out_dir.mkdir(parents=True, exist_ok=True)
    results, crops = [], {}
    for loaded in loaded_images:
        if not loaded.ok:
            continue
        cropped, removed = center_crop_3x4(loaded.image)
        crops[loaded.name] = (cropped, removed)
        for density in DENSITIES:
            result = analyze(loaded.name, loaded.pinned.category, cropped, density, boost)
            write_images(result, cropped, out_dir, docs_dir)
            results.append(result)
    sheets = {}
    for density in DENSITIES:
        by_name = {r.name: r for r in results if r.density == density}
        entries = []
        for loaded in loaded_images:
            if loaded.ok:
                entries.append((loaded.name, crops[loaded.name][0], by_name[loaded.name].indices, ""))
            else:
                entries.append((loaded.name, None, None, loaded.reason))
        path = out_dir / f"contact-{density_label(density)}.png"
        render.contact_sheet(entries, density).save(path)
        sheets[density] = path.relative_to(docs_dir).as_posix()
    return results, crops, sheets
