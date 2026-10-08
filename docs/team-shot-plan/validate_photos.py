#!/usr/bin/env python3
"""Validate a folder of submitted team-shot photos against the shot list.

Folder layout:
    <folder>/manifest.json      photos and releases (see docs/team-shot-plan/RIGHTS.md)
    <folder>/<file>.jpg|png     one photo per shot id
    <folder>/releases/...       the signed release scans or release recordings

Checks: resolution, no EXIF/XMP/IPTC metadata, every photo has a manifest entry
with a CC0 dedication, every person shown has a release on file whose sha256
matches (guardian release for children), no identifiable bystanders, each shot id
exactly once, and the subject/lighting/framing mix against the shot list.

Exit status: 0 = valid, 1 = problems found, 2 = folder or manifest unreadable.
Only the standard library is used.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import imageinfo  # noqa: E402
import shotlist  # noqa: E402

MANIFEST_NAME = "manifest.json"
RELEASE_ROLES = ("adult", "minor_by_guardian")
RELEASE_TYPES = ("signed", "recorded")


class ManifestError(Exception):
    pass


def load_manifest(folder):
    path = os.path.join(folder, MANIFEST_NAME)
    try:
        with open(path, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except FileNotFoundError:
        raise ManifestError("missing %s in %s" % (MANIFEST_NAME, folder))
    except json.JSONDecodeError as exc:
        raise ManifestError("%s is not valid JSON: %s" % (MANIFEST_NAME, exc))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("photos"), list) \
            or not isinstance(manifest.get("releases", []), list):
        raise ManifestError("%s needs a 'photos' list and a 'releases' list" % MANIFEST_NAME)
    return manifest


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_date(value):
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def check_releases(folder, manifest):
    """Return (releases_by_id, errors). Each release must exist on disk and match its sha256."""
    errors = []
    releases = {}
    root = os.path.realpath(folder)
    for rel in manifest.get("releases", []):
        rid = rel.get("id")
        if not rid:
            errors.append("release without an id")
            continue
        if rid in releases:
            errors.append("release %s: duplicate id" % rid)
            continue
        releases[rid] = rel
        if rel.get("type") not in RELEASE_TYPES:
            errors.append("release %s: type must be one of %s" % (rid, list(RELEASE_TYPES)))
        if rel.get("role") not in RELEASE_ROLES:
            errors.append("release %s: role must be one of %s" % (rid, list(RELEASE_ROLES)))
        if rel.get("covers_cc0") is not True:
            errors.append("release %s: must state covers_cc0 = true (CC0 publication)" % rid)
        if rel.get("role") == "minor_by_guardian" and not rel.get("guardian_relationship"):
            errors.append("release %s: child release needs guardian_relationship" % rid)
        if _parse_date(rel.get("signed_on")) is None:
            errors.append("release %s: signed_on must be an ISO date" % rid)
        path = os.path.realpath(os.path.join(folder, rel.get("file") or ""))
        if not rel.get("file") or not path.startswith(root + os.sep):
            errors.append("release %s: 'file' must be a path inside the folder" % rid)
        elif not os.path.isfile(path):
            errors.append("release %s: file %s not found" % (rid, rel["file"]))
        elif not rel.get("sha256"):
            errors.append("release %s: sha256 missing" % rid)
        elif sha256_file(path) != rel["sha256"].lower():
            errors.append("release %s: sha256 does not match %s" % (rid, rel["file"]))
    return releases, errors


def check_photo(folder, entry, shots, releases, limits):
    """Return (errors, warnings, labels) for one manifest photo entry."""
    errors, warnings = [], []
    name = entry.get("file") or "?"
    sid = entry.get("shot_id")
    shot = shots.get(sid)
    labels = None
    if shot is None:
        errors.append("%s: unknown shot_id %r" % (name, sid))
    else:
        labels = {dim: (entry.get("actual") or {}).get(dim, shot[dim])
                  for dim in ("subject", "lighting", "framing")}
        for dim, allowed in (("subject", shotlist.SUBJECTS), ("lighting", shotlist.LIGHTINGS),
                             ("framing", shotlist.FRAMINGS)):
            if labels[dim] not in allowed:
                errors.append("%s: actual %s %r is not a known value" % (name, dim, labels[dim]))
        for dim in labels:
            if labels[dim] != shot[dim]:
                warnings.append("%s: %s is %s, shot list plans %s" % (name, dim, labels[dim], shot[dim]))

    path = os.path.realpath(os.path.join(folder, name))
    if not entry.get("file") or not path.startswith(os.path.realpath(folder) + os.sep):
        return errors + ["%s: 'file' must be a path inside the folder" % name], warnings, labels
    if not os.path.isfile(path):
        return errors + ["%s: file not found" % name], warnings, labels
    try:
        info = imageinfo.inspect_file(path)
    except imageinfo.ImageError as exc:
        return errors + ["%s: %s" % (name, exc)], warnings, labels
    if info.long_edge < limits["min_long_edge_px"] or info.short_edge < limits["min_short_edge_px"]:
        errors.append("%s: %dx%d is below the minimum %dx%d (long x short edge)" % (
            name, info.width, info.height, limits["min_long_edge_px"], limits["min_short_edge_px"]))
    elif info.long_edge < limits["target_long_edge_px"]:
        warnings.append("%s: %dx%d is above the minimum but below the %d px target" % (
            name, info.width, info.height, limits["target_long_edge_px"]))
    if info.metadata:
        errors.append("%s: metadata not stripped (%s)" % (name, ", ".join(info.metadata)))

    if not entry.get("photographer"):
        errors.append("%s: photographer missing" % name)
    taken = _parse_date(entry.get("taken_on"))
    if taken is None:
        errors.append("%s: taken_on must be an ISO date" % name)
    if entry.get("cc0_dedicated") is not True:
        errors.append("%s: cc0_dedicated must be true" % name)
    if entry.get("bystanders_identifiable") is not False:
        errors.append("%s: bystanders_identifiable must be false (reshoot or crop)" % name)

    people = entry.get("people", [])
    minors = 0
    for person in people:
        rid = person.get("release_id")
        rel = releases.get(rid)
        if rel is None:
            errors.append("%s: person has no release on file (release_id %r)" % (name, rid))
            continue
        if rel.get("role") == "minor_by_guardian":
            minors += 1
        signed = _parse_date(rel.get("signed_on"))
        if signed and taken and signed > taken:
            errors.append("%s: release %s is dated after the photo was taken" % (name, rid))
    if shot is not None:
        if len(people) < shot["people"]:
            errors.append("%s: shot %s shows %d people, %d listed" % (name, sid, shot["people"], len(people)))
        if minors < shot["minors"]:
            errors.append("%s: shot %s needs %d child release(s), found %d" % (name, sid, shot["minors"], minors))
        if shot["people"] == 0 and people:
            warnings.append("%s: shot %s is planned without people but lists %d" % (name, sid, len(people)))
    return errors, warnings, labels


def validate_folder(folder, shot_list, allow_partial=False):
    """Validate; return a dict with errors, warnings, mixes and per-shot status."""
    manifest = load_manifest(folder)
    shots = shotlist.shots_by_id(shot_list)
    limits = shot_list["resolution"]
    releases, errors = check_releases(folder, manifest)
    warnings = []
    seen = {}
    submitted = []
    listed_files = set()
    for entry in manifest["photos"]:
        errs, warns, labels = check_photo(folder, entry, shots, releases, limits)
        errors += errs
        warnings += warns
        listed_files.add(entry.get("file"))
        sid = entry.get("shot_id")
        if sid in seen:
            errors.append("%s: shot %s already submitted as %s" % (entry.get("file"), sid, seen[sid]))
        elif labels is not None:
            seen[sid] = entry.get("file")
            submitted.append(labels)
    for fname in sorted(os.listdir(folder)):
        full = os.path.join(folder, fname)
        if os.path.isfile(full) and fname != MANIFEST_NAME and fname not in listed_files \
                and fname.rsplit(".", 1)[-1].lower() in limits["formats"]:
            errors.append("%s: photo in folder but not in the manifest (no release trail)" % fname)
    missing = [sid for sid in shots if sid not in seen]
    if missing and not allow_partial:
        errors.append("missing shots: %s" % ", ".join(missing))
    planned = shotlist.mix_counts(shots.values())
    actual = shotlist.mix_counts(submitted)
    if not allow_partial:
        for dim in planned:
            for value, count in planned[dim].items():
                if actual[dim][value] != count:
                    errors.append("mix %s=%s: %d submitted, shot list plans %d" % (
                        dim, value, actual[dim][value], count))
    return {"errors": errors, "warnings": warnings, "planned": planned, "actual": actual,
            "submitted": len(seen), "missing": missing}


def format_report(result, total):
    lines = ["Submitted shots: %d of %d" % (result["submitted"], total)]
    if result["missing"]:
        lines.append("Missing: " + ", ".join(result["missing"]))
    lines.append("")
    lines.append("Mix (submitted / planned):")
    for dim in result["planned"]:
        cells = ["%s %d/%d" % (value, result["actual"][dim][value], count)
                 for value, count in result["planned"][dim].items()]
        lines.append("  %-9s %s" % (dim, "  ".join(cells)))
    for title, items in (("Warnings", result["warnings"]), ("Errors", result["errors"])):
        if items:
            lines.append("")
            lines.append("%s (%d):" % (title, len(items)))
            lines += ["  - " + item for item in items]
    lines.append("")
    lines.append("RESULT: " + ("FAIL" if result["errors"] else "OK"))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("folder", help="folder holding manifest.json, photos and releases/")
    parser.add_argument("--shot-list", default=shotlist.DEFAULT_SHOT_LIST)
    parser.add_argument("--allow-partial", action="store_true",
                        help="accept a folder with only some shots (skips missing-shot and mix checks)")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)
    try:
        shot_list = shotlist.load_shot_list(args.shot_list)
        if not os.path.isdir(args.folder):
            raise ManifestError("%s is not a folder" % args.folder)
        result = validate_folder(args.folder, shot_list, args.allow_partial)
    except (ManifestError, OSError, ValueError) as exc:
        print("cannot validate: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({k: (v if not isinstance(v, dict) else {d: dict(c) for d, c in v.items()})
                          for k, v in result.items()}, indent=2))
    else:
        print(format_report(result, len(shot_list["shots"])))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
