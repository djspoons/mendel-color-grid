"""Turn the pipeline results into docs/picture-method-results.md (plain Markdown text)."""

import datetime
import statistics

from . import metrics, render
from .palette import CRAYONS
from .pipeline import METHOD, TIMING_REPEATS, density_label
from .preprocess import DENSITIES

CATEGORY_ORDER = ["portrait", "group", "pet or animal", "outdoor", "indoor", "cluttered"]
PRIVACY_EXAMPLES = ["01-astronaut", "02-chelsea-cat", "11-shibuya-crossing"]
PRIVACY_DENSITY = (36, 48)


def _mean(values):
    values = list(values)
    return statistics.fmean(values) if values else float("nan")


def _table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def _pct(x):
    return f"{100 * x:.1f}%"


def _section_inputs(loaded, crops, notes, boost):
    ok = [item for item in loaded if item.ok]
    rows = []
    for item in loaded:
        if item.ok:
            removed = crops[item.name][1]
            rows.append([item.name, f"photos/{item.name}.jpg", item.source, item.license,
                         f"{item.size[0]}x{item.size[1]}", f"`{item.sha256}`",
                         f"crop removes the {removed}", "; ".join(item.notes)])
        else:
            rows.append([item.name, "MISSING", item.source, "-", "-", "-", "-", f"MISSING: {item.reason}"])
    palette_rows = [[i + 1, name, f"`{hex_}`"] for i, (name, hex_) in enumerate(CRAYONS)]
    return "\n".join([
        "## What was read",
        "",
        f"- Images read: {len(ok)} of 11 expected.",
        *["- " + n for n in notes],
        "- " + ("Every image was read and no fallback was taken." if not notes else "Anything not listed above was read normally."),
        f"- Contrast/saturation boost: {boost.describe()}.",
        "- Densities (columns x rows): " + ", ".join(density_label(d) for d in DENSITIES) + ".",
        "- Palette: the classic Crayola 24-count box; hex values below are the ones this run used. "
        "Cell numbers are the 1-24 positions in this list.",
        "",
        _table(["image", "file", "source", "license", "pixels (as saved)", "SHA-256 of saved file",
                "3:4 crop", "notes"], rows),
        "",
        "Palette (number, name, hex):",
        "",
        _table(["#", "crayon", "hex"], palette_rows),
    ])


def _section_method(boost):
    return "\n".join([
        "## Method: average then snap",
        "",
        "1. Center-crop the source to 3:4 portrait (width:height).",
        f"2. Contrast/saturation boost before averaging: **{boost.describe()}**. "
        "The original shown beside each preview is the unboosted crop.",
        "3. Split the cropped picture into the fixed grid and take each cell's mean sRGB color "
        "(plain average of every pixel in the cell).",
        "4. Snap each mean to the nearest of the 24 crayons by Euclidean distance in CIE Lab (D65), not RGB.",
        "",
        "Code: `picture_method/average_then_snap.py` (steps 2-4), `picture_method/preprocess.py` (steps 1 and 3 grid split), "
        "`picture_method/palette.py` (crayons, Lab). Previews, blank grids and metrics are shared code "
        "(`render.py`, `metrics.py`) that any method can reuse.",
        "",
        "Colored preview files are flat cells with no lines. Blank grids are grayscale with uniform thin lines "
        "and the crayon number (1-24) in each cell. Files are under "
        f"`docs/picture-method/{METHOD}/`.",
    ])


def _section_previews(loaded, results, sheets):
    lines = ["## Previews", "", "### Contact sheets (all 11 images, pinned order; original left, preview right)", ""]
    for density in DENSITIES:
        lines += [f"**{density_label(density)}**", "", f"![contact sheet {density_label(density)}]({sheets[density]})", ""]
    lines.append("### Per image and density (original beside colored preview, then blank numbered grid)")
    for item in loaded:
        lines += ["", f"#### {item.name}", ""]
        if not item.ok:
            lines += [f"MISSING: {item.reason}"]
            continue
        for density in DENSITIES:
            r = next(x for x in results if x.name == item.name and x.density == density)
            lines += [f"{density_label(density)}: [blank grid]({r.blank_file})", "",
                      f"![{item.name} {density_label(density)}]({r.compare_file})", ""]
    return "\n".join(lines)


def _section_recognizability(results):
    lines = [
        "## Recognizability notes",
        "",
        "**Automated proxy, not human viewing.** No person or vision model looked at these previews. "
        "A preview counts as recognizable (proxy) when the light/dark pattern survives "
        f"(correlation of Lab lightness between the original's cell means and the snapped crayons >= {metrics.MIN_LUMINANCE_CORR}), "
        f"at least {metrics.MIN_CRAYONS} crayons are used, and the mean Lab distance to the original cell colors is <= "
        f"{metrics.MAX_MEAN_DELTA_E:.0f}. The thresholds are judgment calls. A pass means the picture's large "
        "shapes were kept, not that a child would name the subject; look at the contact sheets for that.",
        "",
    ]
    rows = []
    for r in results:
        why = "recognizable (proxy)" if r.recognizable else "NOT recognizable (proxy): " + "; ".join(r.reasons)
        rows.append([r.name, density_label(r.density), f"{r.corr:.3f}", f"{r.delta_e:.1f}", r.distinct, why])
    lines += [_table(["image", "density", "L correlation", "mean dE", "crayons", "note"], rows), "", "### Roll-up by category", ""]
    rollup = []
    for category in CATEGORY_ORDER:
        for density in DENSITIES:
            group = [r for r in results if r.category == category and r.density == density]
            if group:
                rollup.append([category, density_label(density), ", ".join(sorted({r.name for r in group})),
                               f"{sum(r.recognizable for r in group)}/{len(group)}",
                               f"{_mean(r.corr for r in group):.3f}", f"{_mean(r.delta_e for r in group):.1f}"])
    lines.append(_table(["category", "density", "images", "recognizable (proxy)", "mean L correlation", "mean dE"], rollup))
    return "\n".join(lines)


def _section_palette_usage(results):
    rows = []
    notes = []
    for density in DENSITIES:
        group = [r for r in results if r.density == density]
        if not group:
            continue
        totals = metrics.usage_counts([r.indices for r in group])
        never = [CRAYONS[i][0] for i in range(metrics.N_CRAYONS) if totals[i] == 0]
        rows.append([density_label(density), f"{_mean(r.distinct for r in group):.1f}",
                     _pct(_mean(r.top3 for r in group)), f"{len(never)} of 24",
                     f"{_mean(metrics.N_CRAYONS - r.distinct for r in group):.1f}"])
        notes.append(f"- {density_label(density)} crayons never used on any picture: {', '.join(never) or 'none'}")
    return "\n".join([
        "## Palette usage (average then snap)", "",
        _table(["density", "avg distinct crayons per picture", "avg share of cells in top 3 crayons",
                "crayons never used across all pictures", "avg crayons unused per picture"], rows), "", *notes])


def _section_privacy(results):
    lines = ["## Blank-sheet privacy", ""]
    allowed = {255, render.GRID_GRAY}
    for density in DENSITIES:
        group = [r for r in results if r.density == density]
        if not group:
            continue
        same_geometry = len({r.blank_geometry for r in group}) == 1
        plain = all(set(r.blank_colors) <= allowed for r in group)
        gray = all(r.blank_is_gray for r in group)
        lines.append(
            f"- {density_label(density)}: number-free blank grids of all {len(group)} images are "
            f"{'byte-identical (same cell geometry)' if same_geometry else 'NOT identical'}; "
            f"pixels are only white and one grid gray: {'yes' if plain else 'NO'}; "
            f"sheets are grayscale (no colors): {'yes' if gray else 'NO'}. "
            "Cells are uniform squares; there are no outlines of the subject and no shading.")
    lines += ["", "Leak measured as the share of adjacent cell pairs (left-right and up-down) holding the same number. "
              "The shuffled column is the same numbers placed in random cells (the share with no spatial structure).", ""]
    rows = []
    for density in DENSITIES:
        group = [r for r in results if r.density == density]
        if group:
            observed, shuffled = _mean(r.same_share for r in group), _mean(r.shuffled_share for r in group)
            rows.append([density_label(density), _pct(observed), _pct(shuffled), f"{observed / shuffled:.1f}x"])
    lines += [_table(["density", "avg adjacent-same share", "avg shuffled share", "ratio"], rows), "", "### Three example sheets", ""]
    chosen = [n for n in PRIVACY_EXAMPLES if any(r.name == n for r in results)]
    chosen += [n for n in dict.fromkeys(r.name for r in results) if n not in chosen][: 3 - len(chosen)]
    example_rows = []
    for name in chosen[:3]:
        r = next(x for x in results if x.name == name and x.density == PRIVACY_DENSITY)
        example_rows.append([name, density_label(r.density), f"[{r.blank_file}]({r.blank_file})",
                             _pct(r.same_share), _pct(r.shuffled_share)])
        lines += [f"![blank {name}]({r.blank_file})", ""]
    lines += [_table(["image", "density", "blank sheet", "adjacent-same share", "shuffled share"], example_rows), "",
              "Can the subject be guessed from the numbers alone? **Not tested by a person or model.** What the "
              "numbers show: adjacent cells repeat the same number far more often than chance (ratios above), so "
              "runs and blobs of equal numbers trace the large shapes in the picture (backgrounds, faces, sky). "
              "Outlines of a subject can be inferred from where numbers change, but the colors cannot, and the "
              "identity of a subject has to be guessed from blob shapes. Treat the sheet as leaking shape, not identity."]
    return "\n".join(lines)


def _section_practicality(results):
    rows = []
    for density in DENSITIES:
        group = [r for r in results if r.density == density]
        if group:
            cells = group[0].indices.size
            rows.append([density_label(density), cells, f"{_mean(r.islands for r in group):.1f}",
                         f"{100 * _mean(r.islands for r in group) / cells:.2f}", f"{_mean(r.run_length for r in group):.2f}"])
    per_image = [[r.name, density_label(r.density), r.islands, f"{r.run_length:.2f}"] for r in results]
    return "\n".join([
        "## Practicality for a child", "",
        "An island is a cell whose every existing up/down/left/right neighbour has a different number. "
        "Run length is the average number of consecutive same-numbered cells along a row (all cells / all runs).", "",
        _table(["density", "cells", "avg islands per picture", "islands per 100 cells", "avg row run length"], rows), "",
        "Per image:", "", _table(["image", "density", "islands", "row run length"], per_image)])


def _section_runtime(results):
    rows = [[r.name, density_label(r.density), f"{1000 * r.seconds:.1f}"] for r in results]
    averages = [[density_label(d), f"{1000 * _mean(r.seconds for r in results if r.density == d):.1f}"] for d in DENSITIES]
    return "\n".join([
        "## Runtime", "",
        f"Median of {TIMING_REPEATS} runs of boost + cell averaging + Lab snapping on the already-cropped picture, in ms "
        "(excludes file loading, cropping, rendering and metrics).", "",
        _table(["density", "avg ms per image"], averages), "", "Per image:", "",
        _table(["image", "density", "ms"], rows)])


def _section_verdict(results):
    stats = []
    for density in DENSITIES:
        group = [r for r in results if r.density == density]
        if group:
            stats.append((density, sum(r.recognizable for r in group), len(group), _mean(r.corr for r in group),
                          group[0].indices.size))
    best_count = max(s[1] for s in stats)
    best = min((s for s in stats if s[1] == best_count), key=lambda s: s[4])
    lines = ["## Verdict", "",
             "Rule used: the density with the most recognizable (proxy) pictures; ties go to the one with the fewest cells "
             "(least coloring for a child).", "",
             _table(["density", "recognizable (proxy)", "mean L correlation"],
                    [[density_label(s[0]), f"{s[1]}/{s[2]}", f"{s[3]:.3f}"] for s in stats]), "",
             f"Best density by that rule: **{density_label(best[0])}**. "
             "Higher density keeps more detail (higher correlation) but costs more cells and more single-cell islands; "
             "see the practicality table before choosing."]
    failures = [r for r in results if not r.recognizable]
    if failures:
        lines += ["", "Failure cases (proxy):"] + [
            f"- {r.name} at {density_label(r.density)}: {'; '.join(r.reasons)}" for r in failures]
    else:
        lines += ["", "Failure cases (proxy): none; every picture at every density passed the proxy. "
                  "That does not rule out failures a person would see, especially the cluttered scene at the lowest density."]
    worst = sorted((r for r in results if r.density == best[0]), key=lambda r: r.corr)[:2]
    lines += ["", "Lowest light/dark correlation at the best density: " +
              ", ".join(f"{r.name} ({r.corr:.3f})" for r in worst) + "."]
    return "\n".join(lines)


def build_report(loaded, results, crops, sheets, boost):
    ok = [item for item in loaded if item.ok]
    notes = []
    if not ok:
        notes.append("FAILED READ: none of the 11 pinned images could be loaded; nothing below was produced.")
    for item in loaded:
        if not item.ok:
            notes.append(f"MISSING: {item.name} ({item.source}): {item.reason}. Not substituted; the run continued without it.")
    for item in ok:
        for note in item.notes:
            if "failed" in note:
                notes.append(f"FALLBACK: {item.name}: {note}")
    head = [f"# Picture method results: {METHOD}", "",
            f"Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M UTC} by `python run_picture_method.py`.",
            "Method: average each cell's pixels, then snap that average to the nearest of the 24 Crayola crayons in CIE Lab.", ""]
    if not ok:
        return "\n".join(head + [_section_inputs(loaded, crops, notes, boost)]) + "\n"
    parts = [_section_inputs(loaded, crops, notes, boost), _section_method(boost), _section_previews(loaded, results, sheets),
             _section_recognizability(results), _section_palette_usage(results), _section_privacy(results),
             _section_practicality(results), _section_runtime(results), _section_verdict(results)]
    return "\n".join(head) + "\n" + "\n\n".join(parts) + "\n"
