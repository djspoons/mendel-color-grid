"""Shared test helpers: synthetic JPEG/PNG bytes and a valid submission folder."""
import hashlib
import json
import os
import struct
import sys
import zlib

PLAN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "team-shot-plan")
if PLAN_DIR not in sys.path:
    sys.path.insert(0, PLAN_DIR)

import shotlist  # noqa: E402


def _segment(marker, payload):
    return bytes([0xFF, marker]) + struct.pack(">H", len(payload) + 2) + payload


def make_jpeg(width=2400, height=1600, exif=False, xmp=False):
    out = b"\xff\xd8" + _segment(0xE0, b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00")
    if exif:
        out += _segment(0xE1, b"Exif\x00\x00" + b"II*\x00\x08\x00\x00\x00")
    if xmp:
        out += _segment(0xE1, b"http://ns.adobe.com/xap/1.0/\x00<x/>")
    out += _segment(0xC0, b"\x08" + struct.pack(">HH", height, width) + b"\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01")
    out += _segment(0xDA, b"\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00")
    return out + b"\x12\x34\x56" + b"\xff\xd9"


def make_png(width=2400, height=1600, text=False):
    def chunk(ctype, body):
        return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", zlib.crc32(ctype + body))
    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    if text:
        out += chunk(b"tEXt", b"Software\x00camera")
    return out + chunk(b"IDAT", b"") + chunk(b"IEND", b"")


def write_valid_submission(folder, shot_list=None):
    """Write a folder that passes validate_photos for every shot. Returns the manifest dict."""
    shot_list = shot_list or shotlist.load_shot_list()
    os.makedirs(os.path.join(folder, "releases"), exist_ok=True)
    releases = []
    for rid, role in (("R-001", "adult"), ("R-002", "minor_by_guardian")):
        rel_path = os.path.join("releases", rid + ".pdf")
        data = ("release " + rid).encode()
        with open(os.path.join(folder, rel_path), "wb") as handle:
            handle.write(data)
        rel = {"id": rid, "type": "signed", "role": role, "file": rel_path,
               "sha256": hashlib.sha256(data).hexdigest(), "signed_on": "2025-06-01", "covers_cc0": True}
        if role == "minor_by_guardian":
            rel["guardian_relationship"] = "parent"
        releases.append(rel)
    photos = []
    for shot in shot_list["shots"]:
        name = shot["id"] + ".jpg"
        with open(os.path.join(folder, name), "wb") as handle:
            handle.write(make_jpeg())
        people = [{"release_id": "R-002"}] * shot["minors"] + [{"release_id": "R-001"}] * (shot["people"] - shot["minors"])
        photos.append({"file": name, "shot_id": shot["id"], "photographer": "Test Photographer",
                       "taken_on": "2025-06-06", "cc0_dedicated": True, "bystanders_identifiable": False,
                       "people": people})
    manifest = {"releases": releases, "photos": photos}
    write_manifest(folder, manifest)
    return manifest


def write_manifest(folder, manifest):
    with open(os.path.join(folder, "manifest.json"), "w", encoding="utf-8") as handle:
        json.dump(manifest, handle)
