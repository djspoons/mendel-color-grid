"""Regenerate docs/picture-method-results.md and the images beside it.

Method: average then snap. Run with `python run_picture_method.py` from the repo root.
"""

import sys
from pathlib import Path

from picture_method.average_then_snap import DEFAULT_BOOST
from picture_method.inputs import load_all
from picture_method.pipeline import run_all
from picture_method.report import build_report

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
REPORT = DOCS / "picture-method-results.md"


def main():
    loaded = load_all(ROOT / "photos")
    results, crops, sheets = run_all(loaded, DOCS, DEFAULT_BOOST)
    text = build_report(loaded, results, crops, sheets, DEFAULT_BOOST)
    DOCS.mkdir(exist_ok=True)
    REPORT.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {REPORT.relative_to(ROOT)} and images under docs/picture-method/")
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
