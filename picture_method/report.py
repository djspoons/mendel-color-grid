"""Builds docs/picture-method-results.md from the run's records (plain Markdown text)."""

import datetime

import numpy as np

from .palette import CRAYONS

CATEGORY_ORDER = ["portrait", "group", "pet or animal", "outdoor", "indoor", "cluttered"]


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else float("nan")


def _density(d):
    return f"{d[0]}x{d[1]}"


def _rec_by_density(records, d):
    return [r for r in records if r["density"] == d]


def section_inputs(sources, densities, method_dir, params):
    out = ["# Picture method results: quantize then majority vote", ""]
    ok = [s for s in sources if s.status == "OK"]
    out.append(f"Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC by `python run_picture_method.py`.")
    out += ["", "## What was read", "", f"- Images read: **{len(ok)}** (expected 11)."]
    for s in sources:
        if s.status != "OK":
            out.append(f"- **MISSING** {s.spec.filename}: {s.reason}")
    if len(ok) != 11:
        out.append("- **PARTIAL RUN**: not all 11 pinned images were read; missing ones are marked, none were substituted.")
    out += ["", "| # | file | category | source | license | fetched size | original size | SHA-256 (file) | SHA-256 (decoded RGB) | crop to 3:4 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for s in sources:
        if s.status == "OK":
            out.append(
                f"| {s.spec.number:02d} | photos/{s.spec.filename} | {s.spec.category} | {s.source} | {s.license} | "
                f"{s.width}x{s.height} | {s.original_size or 'n/a'} | `{s.sha256}` | `{s.pixel_sha256}` | {s.crop_note} |"
            )
        else:
            out.append(f"| {s.spec.number:02d} | photos/{s.spec.filename} | {s.spec.category} | MISSING | | | | | | |")
    out += ["", "Bundled images are re-encoded to JPEG (quality 95) when saved, so their file hash depends on the Pillow build; the decoded-RGB hash is of the library's original array and is the one to compare.", ""]
    out += ["### Palette: Crayola 24-count box", "", "| # | crayon | hex |", "|---|---|---|"]
    out += [f"| {i + 1} | {n} | {h} |" for i, (n, h) in enumerate(CRAYONS)]
    out += ["", "Cell numbers are these 1-24 indexes.", "", f"### Densities (columns x rows): {', '.join(_density(d) for d in densities)}", ""]
    out += [
        "### Method",
        "",
        "Pre-processing: center-crop to 3:4 portrait, then Lanczos-resize to "
        f"(cols x {params['subpixels']}) by (rows x {params['subpixels']}) pixels, i.e. {params['subpixels']}x{params['subpixels']} pixels per cell.",
        "1. Quantize: every pixel of that small image is mapped to the nearest of the 24 crayons (Euclidean distance in CIE Lab, D65).",
        "2. Vote: each cell takes the crayon most common among its pixels. A tie goes to the tied crayon with the larger pixel share in the 8 neighboring cells; a remaining tie goes to the lower palette number.",
        "3. Alternative (reported separately): Floyd-Steinberg dithering in Lab during step 1, then the same vote.",
        f"Previews and sheets are in `{method_dir}/`. Main results below are WITHOUT dithering.",
        "",
    ]
    return out


def section_per_image(records, method_dir, rel):
    out = ["## Per image and density", "", "Original (3:4 crop) beside the colored preview (standalone preview PNGs sit in the same folder), and the blank numbered grid. Recognizability is a computed proxy (see next section).", ""]
    numbers = sorted({r["item"].spec.number for r in records})
    for n in numbers:
        recs = [r for r in records if r["item"].spec.number == n]
        item = recs[0]["item"]
        out += [f"### {item.spec.number:02d} {item.spec.name} ({item.spec.category})", "", "| density | original beside colored preview | blank grid | runtime | recognizability |", "|---|---|---|---|---|"]
        for r in recs:
            f = r["files"]
            out.append(
                f"| {_density(r['density'])} | ![]({rel(f['side_by_side'])}) | ![]({rel(f['blank'])}) | "
                f"{r['plain']['seconds'] * 1000:.0f} ms | {r['recog'][0]}" + (f": {'; '.join(r['recog'][1])}" if r["recog"][1] else "") + " |"
            )
        out.append("")
    return out


def section_sheets(densities, sheet_files, rel):
    out = ["## Contact sheets (all 11 images, pinned order, 4 per row)", ""]
    for d in densities:
        out += [f"### {_density(d)}", "", f"![]({rel(sheet_files[d])})", ""]
    return out


def section_recognizability(records, densities):
    out = ["## Recognizability notes", "", "Computed, not eyeballed: the verdict uses the correlation of preview lightness with the original's cell lightness (>=0.85 recognizable, >=0.70 partly) and flags speckle (>8% single-cell islands), <=5 crayons, or top-3 crayons >85% of cells. Treat as a screening proxy and check the contact sheets by eye.", "", "### By category", "", "| category | " + " | ".join(_density(d) for d in densities) + " |", "|---|" + "---|" * len(densities)]
    for cat in CATEGORY_ORDER:
        cells = []
        for d in densities:
            rs = [r for r in _rec_by_density(records, d) if r["item"].spec.category == cat]
            if not rs:
                cells.append("n/a")
                continue
            tally = {}
            for r in rs:
                tally[r["recog"][0]] = tally.get(r["recog"][0], 0) + 1
            cells.append(f"{', '.join(f'{v} {k}' for k, v in tally.items())}; lightness r {mean(r['plain']['lightness_corr'] for r in rs):.2f}")
        out.append(f"| {cat} | " + " | ".join(cells) + " |")
    out += ["", "### Per image", "", "| image | " + " | ".join(_density(d) for d in densities) + " |", "|---|" + "---|" * len(densities)]
    for n in sorted({r["item"].spec.number for r in records}):
        cells = []
        for d in densities:
            r = next(r for r in records if r["item"].spec.number == n and r["density"] == d)
            note = r["recog"][0] + (f" ({'; '.join(r['recog'][1])})" if r["recog"][1] else "")
            cells.append(f"{note}, r={r['plain']['lightness_corr']:.2f}, dE={r['plain']['delta_e']:.1f}")
        out.append(f"| {r['item'].spec.number:02d} {r['item'].spec.name} | " + " | ".join(cells) + " |")
    return out + [""]


def section_palette_usage(records, densities):
    out = ["## Palette usage", "", "| density | avg distinct crayons per picture | avg share of cells in top 3 crayons | avg crayons unused per picture | crayons never used in any picture |", "|---|---|---|---|---|"]
    for d in densities:
        rs = _rec_by_density(records, d)
        used = np.zeros(24, dtype=bool)
        for r in rs:
            used |= np.bincount(r["plain"]["grid"].ravel(), minlength=24) > 0
        never = [CRAYONS[i][0] for i in range(24) if not used[i]]
        out.append(
            f"| {_density(d)} | {mean(r['plain']['distinct'] for r in rs):.1f} | {mean(r['plain']['top3'] for r in rs) * 100:.0f}% | "
            f"{24 - mean(r['plain']['distinct'] for r in rs):.1f} | {len(never)}" + (f" ({', '.join(never)})" if never else "") + " |"
        )
    return out + [""]


def _excerpt(grid, rows=10):
    return "\n".join(" ".join(f"{int(v) + 1:2d}" for v in row) for row in grid[:rows])


def section_privacy(records, densities, blank_checks, examples, rel):
    out = ["## Blank-sheet privacy", ""]
    for d in densities:
        ok, total = blank_checks[d]
        out.append(f"- {_density(d)}: {ok}/{total} blank grids pass the geometry check (identical pixel size per density, grayscale only, the outer 2 px ring of every cell is pure white, so no outlines, grid lines or shading; only the digits differ).")
    out += ["", "Leak measure: share of horizontally/vertically adjacent cell pairs carrying the same number, against the share expected if the same numbers were scattered at random.", "", "| density | adjacent same-number share | random-scatter baseline | ratio |", "|---|---|---|---|"]
    for d in densities:
        rs = _rec_by_density(records, d)
        a, c = mean(r["plain"]["same_adjacent"] for r in rs), mean(r["plain"]["chance_adjacent"] for r in rs)
        out.append(f"| {_density(d)} | {a * 100:.0f}% | {c * 100:.0f}% | {a / c:.1f}x |")
    out += ["", "Can the subject be guessed from the numbers alone? Not tested by a person or model here. What is measured: the numbers form large same-number regions (ratio above), so shapes and light/dark layout are readable in the digits for anyone who looks for them; the digits do not name colors, so material, identity and color are not given away.", ""]
    out.append("Example sheets (first 10 rows of the first density; full sheets are the blank PNGs):")
    for r in examples:
        out += ["", f"{r['item'].spec.number:02d} {r['item'].spec.name} ({_density(r['density'])}), blank PNG: `{r['files']['blank_rel']}`", "", f"![]({rel(r['files']['blank'])})", "", "```", _excerpt(r["plain"]["grid"]), "```"]
    return out + [""]


def section_practicality(records, densities):
    out = ["## Practicality for a child", "", "| density | cells | avg single-cell islands per picture | islands as share of cells | avg run length along a row (cells) |", "|---|---|---|---|---|"]
    for d in densities:
        rs = _rec_by_density(records, d)
        out.append(f"| {_density(d)} | {d[0] * d[1]} | {mean(r['plain']['islands'] for r in rs):.0f} | {mean(r['plain']['island_share'] for r in rs) * 100:.1f}% | {mean(r['plain']['run_length'] for r in rs):.2f} |")
    tie = {d: mean(r["plain"]["tie_cells"] / (d[0] * d[1]) for r in _rec_by_density(records, d)) for d in densities}
    return out + ["", "An island is a cell whose every existing up/down/left/right neighbor has a different number.", "Cells that needed the neighbor tie-break: " + ", ".join(f"{_density(d)} {tie[d] * 100:.1f}%" for d in densities) + ".", ""]


def section_runtime(records, densities):
    out = ["## Runtime (resize + quantize + vote, no image decoding; ms)", "", "| image | " + " | ".join(_density(d) for d in densities) + " |", "|---|" + "---|" * len(densities)]
    for n in sorted({r["item"].spec.number for r in records}):
        cells = [f"{next(r for r in records if r['item'].spec.number == n and r['density'] == d)['plain']['seconds'] * 1000:.0f}" for d in densities]
        name = next(r for r in records if r["item"].spec.number == n)["item"].spec.name
        out.append(f"| {n:02d} {name} | " + " | ".join(cells) + " |")
    out.append("| mean | " + " | ".join(f"{mean(r['plain']['seconds'] for r in _rec_by_density(records, d)) * 1000:.0f}" for d in densities) + " |")
    return out + [""]


def section_dither(records, densities):
    keys = [("lightness_corr", "lightness r", "{:.3f}"), ("delta_e", "mean dE to original", "{:.1f}"), ("island_share", "island share", "{:.1%}"), ("run_length", "row run length", "{:.2f}"), ("same_adjacent", "adjacent same-number", "{:.1%}"), ("distinct", "distinct crayons", "{:.1f}"), ("seconds", "runtime s", "{:.2f}")]
    out = ["## Dithering comparison (Floyd-Steinberg in Lab vs none)", "", "| density | metric | no dither | dither |", "|---|---|---|---|"]
    verdicts = []
    for d in densities:
        rs = _rec_by_density(records, d)
        for key, label, fmt in keys:
            out.append(f"| {_density(d)} | {label} | {fmt.format(mean(r['plain'][key] for r in rs))} | {fmt.format(mean(r['dither'][key] for r in rs))} |")
        dr = mean(r["dither"]["lightness_corr"] - r["plain"]["lightness_corr"] for r in rs)
        di = mean(r["dither"]["island_share"] - r["plain"]["island_share"] for r in rs)
        verdicts.append(f"- {_density(d)}: dithering changes lightness r by {dr:+.3f} and island share by {di * 100:+.1f} points: " + ("helps recognizability without adding speckle." if dr > 0 and di <= 0 else "hurts or is mixed (more speckle and/or lower correlation); the majority vote already averages tones within a cell."))
    return out + ["", *verdicts, ""]


def section_verdict(records, densities):
    out = ["## Verdict", ""]
    scores = {d: mean(r["plain"]["lightness_corr"] for r in _rec_by_density(records, d)) - 2 * mean(r["plain"]["island_share"] for r in _rec_by_density(records, d)) for d in densities}
    best = max(scores, key=scores.get)
    out.append("Density score = mean lightness r minus 2 x mean island share (heuristic, stated so it can be challenged): " + ", ".join(f"{_density(d)} = {scores[d]:.3f}" for d in densities) + f". Best by this score: **{_density(best)}**. Finer grids keep more detail but cost the child more cells; the island and run-length tables show the trade.")
    fails = [r for r in _rec_by_density(records, best) if r["recog"][0] != "recognizable"]
    out.append("")
    if fails:
        out.append(f"Failure cases at {_density(best)}:")
        out += [f"- {r['item'].spec.number:02d} {r['item'].spec.name}: {r['recog'][0]}" + (f" ({'; '.join(r['recog'][1])})" if r["recog"][1] else "") for r in fails]
    else:
        out.append(f"No image failed the recognizability proxy at {_density(best)}.")
    collapsed = [f"{r['item'].spec.number:02d} {r['item'].spec.name} @ {_density(r['density'])}" for r in records if r["plain"]["distinct"] <= 6]
    out.append("")
    out.append("Palette collapse (6 or fewer crayons used): " + (", ".join(collapsed) if collapsed else "none."))
    return out + [""]


def build_report(sources, records, densities, method_dir, params, sheet_files, blank_checks, examples, rel):
    parts = [
        section_inputs(sources, densities, method_dir, params),
        section_per_image(records, method_dir, rel),
        section_sheets(densities, sheet_files, rel),
        section_recognizability(records, densities),
        section_palette_usage(records, densities),
        section_privacy(records, densities, blank_checks, examples, rel),
        section_practicality(records, densities),
        section_runtime(records, densities),
        section_dither(records, densities),
        section_verdict(records, densities),
    ]
    return "\n".join(line for part in parts for line in part) + "\n"
