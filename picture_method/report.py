"""Build the comparable markdown report (docs/picture-method-results.md)."""

import datetime
import platform

import numpy as np

from . import color, config, metrics, render

MAX_ISLAND_SHARE = 0.03  # verdict: a density is practical if <= 3% of cells are islands


def density_label(density):
    return f"{density[0]}x{density[1]}"


def _table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return lines


def _mean(values):
    values = list(values)
    return float(np.mean(values)) if values else float("nan")


def input_section(images):
    read = [i for i in images if not i.missing]
    lines = ["## What was read", "",
             f"- Images read: **{len(read)}** (expected {len(config.IMAGES)})",
             f"- Densities (columns x rows): {', '.join(density_label(d) for d in config.DENSITIES)}",
             "- Pre-processing: center-crop to 3:4 portrait (width:height), then resize to the grid "
             f"(each cell analysed from a {config.SUPERSAMPLE}x{config.SUPERSAMPLE} pixel block, Lanczos).",
             "", "### Images", ""]
    rows = []
    for i in images:
        s = i.spec
        if i.missing:
            rows.append([s.number, s.filename, s.category, i.source, "MISSING", "-", "-",
                         i.missing_reason])
        else:
            rows.append([s.number, s.filename, s.category, i.source, i.license,
                         f"{i.size[0]}x{i.size[1]}", f"`{i.sha256}`",
                         i.crop_note + (f"; {i.note}" if i.note else "")])
    lines += _table(["#", "file", "category", "source", "license", "pixels", "SHA-256", "crop / note"], rows)
    lines += ["", "### Palette: Crayola 24-count (cell number = index)", ""]
    lines += _table(["#", "name", "hex"],
                    [[n + 1, name, f"#{hx}"] for n, (name, hx) in enumerate(config.PALETTE)])
    return lines


def method_section():
    from . import edge_aware as ea
    return ["## Method: edge-aware cell coloring", "",
            f"1. Sobel magnitude on a luminance copy, averaged per cell. Cells at or above the "
            f"{ea.EDGE_PERCENTILE}th percentile of strength (and at least {ea.EDGE_FLOOR}) are edge cells.",
            "2. Edge cells: split the cell's pixels at the block's mean luminance; a cell darker than its "
            f"{ea.NEIGHBOURHOOD}x{ea.NEIGHBOURHOOD} neighbourhood takes the dominant crayon of its darker side, "
            "any other edge cell the dominant crayon of its lighter side (dominant = most common nearest crayon "
            "among that side's pixels).",
            "3. Flat cells: mean of the block in Lab, snapped to the nearest crayon (CIE76 distance in Lab).",
            "4. Smoothing: one pass recolors single-cell islands (no 4-neighbour of the same crayon) to their "
            "most common neighbour crayon, unless the cell is an edge cell.",
            "", "Edge detector used: Sobel (scikit-image). Runtime covers resize + coloring, not rendering."]


def per_image_section(records, sheets):
    lines = ["## Previews, originals and blank grids", "",
             "Each comparison image shows the original (left) beside the colored preview (right). "
             "The blank grid shows numbers only.", ""]
    stems = []
    for recs in records.values():
        for r in recs:
            if r.loaded.spec.stem not in stems:
                stems.append(r.loaded.spec.stem)
    for stem in stems:
        lines += [f"### {stem}", ""]
        for density, recs in records.items():
            r = next((x for x in recs if x.loaded.spec.stem == stem), None)
            if r is None:
                continue
            verdict = "recognizable (proxy)" if r.recognizable else f"NOT recognizable (proxy): {r.reason}"
            lines += [f"**{density_label(density)}** - edge rule on {r.result.n_edge_cells} of "
                      f"{r.indices.size} cells, {r.result.n_smoothed} islands smoothed, "
                      f"{r.runtime * 1000:.0f} ms; {verdict}", "",
                      f"![{stem} {density_label(density)} original | preview]({r.files['compare']})",
                      f"![{stem} {density_label(density)} blank grid]({r.files['blank']})", ""]
    lines += ["## Contact sheets", "",
              "All images in pinned order, original | preview in each tile.", ""]
    for density, path in sheets.items():
        lines += [f"### {density_label(density)}", "", f"![contact sheet {density_label(density)}]({path})", ""]
    return lines


def recognizability_section(records):
    lines = ["## Recognizability notes", "",
             "These notes are an AUTOMATED PROXY, not a human viewing. A preview counts as recognizable when, "
             f"against the original's per-cell mean, its luminance SSIM is >= {metrics.SSIM_MIN}, the correlation "
             f"of Sobel edge maps is >= {metrics.EDGE_CORR_MIN} and at least {metrics.MIN_CRAYONS} crayons are used. "
             "Look at the contact sheets to confirm by eye.", "",
             "### Per image and density", ""]
    rows = []
    for density, recs in records.items():
        for r in recs:
            rows.append([r.loaded.spec.stem, density_label(density),
                         "yes" if r.recognizable else "no", f"{r.fid.luma_ssim:.2f}",
                         f"{r.fid.edge_corr:.2f}", f"{r.fid.mean_delta_e:.1f}", r.reason or "-"])
    lines += _table(["image", "density", "recognizable", "luma SSIM", "edge corr", "mean dE76", "why not"], rows)
    lines += ["", "### Roll-up by category (recognizable / total)", ""]
    header = ["category"] + [density_label(d) for d in records]
    rows = []
    for category in config.CATEGORY_ORDER:
        row = [category]
        for recs in records.values():
            sel = [r for r in recs if r.loaded.spec.category == category]
            row.append(f"{sum(r.recognizable for r in sel)}/{len(sel)}" if sel else "n/a")
        rows.append(row)
    lines += _table(header, rows)
    return lines


def palette_section(records):
    lines = ["## Palette usage", ""]
    rows = []
    for density, recs in records.items():
        if not recs:
            continue
        total = sum(metrics.palette_counts(r.indices) for r in recs)
        unused = [color.PALETTE_NAMES[i] for i in np.flatnonzero(total == 0)]
        rows.append([density_label(density),
                     f"{_mean(metrics.distinct_crayons(r.indices) for r in recs):.1f}",
                     f"{100 * _mean(metrics.top3_share(r.indices) for r in recs):.1f}%",
                     len(unused), ", ".join(unused) or "-"])
    lines += _table(["density", "avg distinct crayons / picture", "avg share of cells in top-3 crayons",
                     "crayons never used (all pictures)", "which"], rows)
    return lines


def privacy_section(records):
    lines = ["## Blank-sheet privacy", ""]
    for density, recs in records.items():
        if recs:
            ok, msg = render.check_blank_geometry([r.blank for r in recs], *density)
            lines.append(f"- {density_label(density)}: {'OK' if ok else 'FAILED'} - {msg}")
    lines += ["", "Blank grids contain only numbers on white cells with uniform grey grid lines; "
              "no outlines, shading or colors.", "",
              "Leakage = share of adjacent cell pairs (horizontal + vertical) carrying the same number. "
              "'Chance' is the share expected if the same numbers were shuffled over the grid; the excess "
              "is the structure the layout gives away.", ""]
    rows = []
    for density, recs in records.items():
        if recs:
            share = _mean(metrics.adjacent_same_share(r.indices) for r in recs)
            chance = _mean(metrics.chance_same_share(r.indices) for r in recs)
            rows.append([density_label(density), f"{100 * share:.1f}%", f"{100 * chance:.1f}%",
                         f"{100 * (share - chance):+.1f} pts"])
    lines += _table(["density", "adjacent same-number share (avg)", "chance", "excess"], rows)
    mid = config.DENSITIES[1]
    recs = records.get(mid) or []
    if recs:
        ordered = sorted(recs, key=lambda r: metrics.adjacent_same_share(r.indices))
        examples = [("least leaky", ordered[0]), ("median", ordered[len(ordered) // 2]),
                    ("most leaky", ordered[-1])]
        lines += ["", f"Example blank sheets at {density_label(mid)}:", ""]
        for label, r in examples:
            lines += [f"**{r.loaded.spec.stem}** ({label}, {100 * metrics.adjacent_same_share(r.indices):.1f}% "
                      f"adjacent same-number)", "", f"![blank {r.loaded.spec.stem}]({r.files['blank']})", ""]
    lines += ["Can the subject be guessed from the numbers alone? NOT TESTED: this script has no human or model "
              "viewer. The excess over chance shows that regions of equal numbers are readable as shapes; "
              "a high excess means large same-number patches that outline the subject's major regions."]
    return lines


def practicality_section(records):
    lines = ["## Practicality for a child", "",
             "Island = a cell with no 4-neighbour of the same crayon. Run length = average length of "
             "same-number runs along a row.", ""]
    rows = []
    for density, recs in records.items():
        if recs:
            rows.append([density_label(density),
                         f"{_mean(metrics.count_islands(r.indices) for r in recs):.1f}",
                         f"{100 * _mean(metrics.count_islands(r.indices) / r.indices.size for r in recs):.2f}%",
                         f"{_mean(metrics.mean_run_length(r.indices) for r in recs):.2f}"])
    lines += _table(["density", "avg islands / picture", "islands as share of cells", "avg run length (cells)"], rows)
    lines += ["", "### Per image", ""]
    rows = []
    for density, recs in records.items():
        for r in recs:
            rows.append([r.loaded.spec.stem, density_label(density), metrics.count_islands(r.indices),
                         f"{metrics.mean_run_length(r.indices):.2f}",
                         f"{r.result.n_edge_cells} ({100 * r.result.n_edge_cells / r.indices.size:.0f}%)",
                         r.result.n_smoothed])
    lines += _table(["image", "density", "islands", "avg run length", "cells using edge rule", "islands smoothed"], rows)
    return lines


def runtime_section(records):
    lines = ["## Runtime per image (seconds, resize + coloring)", ""]
    names = []
    for recs in records.values():
        for r in recs:
            if r.loaded.spec.stem not in names:
                names.append(r.loaded.spec.stem)
    rows = []
    for stem in names:
        row = [stem]
        for recs in records.values():
            r = next((x for x in recs if x.loaded.spec.stem == stem), None)
            row.append(f"{r.runtime:.2f}" if r else "n/a")
        rows.append(row)
    return lines + _table(["image"] + [density_label(d) for d in records], rows)


def edge_rule_section(records):
    lines = ["## Edge rule usage", ""]
    rows = []
    for density, recs in records.items():
        if recs:
            rows.append([density_label(density),
                         f"{_mean(r.result.n_edge_cells for r in recs):.0f}",
                         f"{100 * _mean(r.result.n_edge_cells / r.indices.size for r in recs):.1f}%",
                         f"{_mean(r.result.n_smoothed for r in recs):.1f}"])
    return lines + _table(["density", "avg cells on edge rule", "share of cells", "avg islands smoothed"], rows)


def verdict_section(records):
    lines = ["## Verdict", ""]
    scored = []
    for density, recs in records.items():
        if recs:
            island = _mean(metrics.count_islands(r.indices) / r.indices.size for r in recs)
            ssim = _mean(r.fid.luma_ssim for r in recs)
            ok = sum(r.recognizable for r in recs)
            scored.append((density, island, ssim, ok, len(recs)))
    if not scored:
        return lines + ["No image could be processed; no verdict."]
    practical = [s for s in scored if s[1] <= MAX_ISLAND_SHARE]
    best = max(practical, key=lambda s: (s[3], s[2])) if practical else min(scored, key=lambda s: s[1])
    lines.append(f"Rule: among densities with at most {100 * MAX_ISLAND_SHARE:.0f}% island cells, pick the one with "
                 "the most recognizable (proxy) pictures, then the highest luminance SSIM.")
    for density, island, ssim, ok, n in scored:
        lines.append(f"- {density_label(density)}: {ok}/{n} recognizable, luminance SSIM {ssim:.2f}, "
                     f"islands {100 * island:.2f}% of cells")
    lines.append(f"- **Best density by this rule: {density_label(best[0])}.**")
    failures = [f"{r.loaded.spec.stem} @ {density_label(d)}" for d, recs in records.items()
                for r in recs if not r.recognizable]
    lines.append("- Failure cases (proxy): " + (", ".join(failures) if failures else "none"))
    return lines


def fallback_notes(images):
    notes = []
    for i in images:
        if i.missing:
            notes.append(f"{i.spec.filename}: MISSING - {i.missing_reason}")
        elif i.license.startswith("unknown"):
            notes.append(f"{i.spec.filename}: license not determined - {i.license}")
    read = sum(not i.missing for i in images)
    if read < len(images):
        notes.append(f"Only {read} of {len(images)} images could be read; results cover those only. "
                     "No substitute images were used.")
    return notes


def build_report(images, records, sheets):
    lines = ["# Picture method results: edge-aware cell coloring", "",
             f"Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M UTC} "
             f"(Python {platform.python_version()}). Regenerate with `python -m picture_method`.", ""]
    notes = fallback_notes(images)
    if notes:
        lines += ["## Read problems / fallbacks", ""] + [f"- {n}" for n in notes] + [""]
    sections = [input_section(images), method_section(), per_image_section(records, sheets),
                recognizability_section(records), palette_section(records), privacy_section(records),
                practicality_section(records), edge_rule_section(records), runtime_section(records),
                verdict_section(records)]
    for section in sections:
        lines += section + [""]
    return "\n".join(lines)
