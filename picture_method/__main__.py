"""Entry point: python -m picture_method"""

import re
import sys

from . import config, inputs, pipeline, report


def broken_links(text):
    """Relative image links in the report whose file does not exist."""
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    return [l for l in links if not (config.DOCS_DIR / l).exists()]


def main():
    config.OUT_DIR.mkdir(parents=True, exist_ok=True)
    images = inputs.load_all()
    records = pipeline.run_all(images)
    if not any(records.values()):
        print("No image could be read; nothing to report.", file=sys.stderr)
        for i in images:
            print(f"{i.spec.filename}: {i.missing_reason}", file=sys.stderr)
        return 1
    sheets = pipeline.write_contact_sheets(records)
    text = report.build_report(images, records, sheets)
    broken = broken_links(text)
    if broken:
        text += "\n\n## Broken image links\n\n" + "\n".join(f"- {l}" for l in broken)
    config.REPORT_PATH.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\nWrote {config.REPORT_PATH} and previews under {config.OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
