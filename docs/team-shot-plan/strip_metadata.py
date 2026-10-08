#!/usr/bin/env python3
"""Losslessly remove EXIF, XMP, IPTC and comment segments from JPEG files.

Usage: strip_metadata.py IN.jpg [IN2.jpg ...] --out-dir OUT
Rotate pixels upright first: stripping drops the EXIF orientation flag.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import imageinfo  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("files", nargs="+")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args(argv)
    os.makedirs(args.out_dir, exist_ok=True)
    failures = 0
    for path in args.files:
        try:
            with open(path, "rb") as handle:
                clean = imageinfo.strip_jpeg_metadata(handle.read())
            target = os.path.join(args.out_dir, os.path.basename(path))
            with open(target, "wb") as handle:
                handle.write(clean)
            print("stripped %s -> %s" % (path, target))
        except (OSError, imageinfo.ImageError) as exc:
            failures += 1
            print("FAILED %s: %s" % (path, exc), file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
