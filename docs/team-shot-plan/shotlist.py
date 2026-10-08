"""Load, validate and summarise the team-shot list (docs/team-shot-plan/shot_list.json)."""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SHOT_LIST = os.path.join(HERE, "shot_list.json")

SUBJECTS = ("single_child", "group", "adults_with_children", "pets", "objects")
LIGHTINGS = ("bright", "indoor", "low_light", "backlit")
FRAMINGS = ("close-up", "medium", "wide")
SHOT_COUNT = 20


def load_shot_list(path=DEFAULT_SHOT_LIST):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    problems = validate_shot_list(data)
    if problems:
        raise ValueError("invalid shot list %s: %s" % (path, "; ".join(problems)))
    return data


def validate_shot_list(data):
    """Return a list of problems; empty when the shot list is usable."""
    problems = []
    shots = data.get("shots")
    if not isinstance(shots, list):
        return ["'shots' must be a list"]
    if len(shots) != SHOT_COUNT:
        problems.append("expected %d shots, found %d" % (SHOT_COUNT, len(shots)))
    seen = set()
    for shot in shots:
        sid = shot.get("id", "?")
        if sid in seen:
            problems.append("duplicate shot id %s" % sid)
        seen.add(sid)
        for key, allowed in (("subject", SUBJECTS), ("lighting", LIGHTINGS), ("framing", FRAMINGS)):
            if shot.get(key) not in allowed:
                problems.append("%s: %s %r not in %s" % (sid, key, shot.get(key), list(allowed)))
        for key in ("scene", "query"):
            if not shot.get(key):
                problems.append("%s: missing %s" % (sid, key))
        if not isinstance(shot.get("people"), int) or not isinstance(shot.get("minors"), int):
            problems.append("%s: people and minors must be integers" % sid)
        elif shot["minors"] > shot["people"]:
            problems.append("%s: minors exceeds people" % sid)
    res = data.get("resolution", {})
    for key in ("min_long_edge_px", "min_short_edge_px", "target_long_edge_px"):
        if not isinstance(res.get(key), int):
            problems.append("resolution.%s must be an integer" % key)
    return problems


def mix_counts(labelled):
    """Count subject/lighting/framing over dicts that carry those three keys.

    Every allowed value appears in the result, with zero when absent.
    """
    out = {"subject": Counter(dict.fromkeys(SUBJECTS, 0)),
           "lighting": Counter(dict.fromkeys(LIGHTINGS, 0)),
           "framing": Counter(dict.fromkeys(FRAMINGS, 0))}
    for item in labelled:
        for dim in out:
            out[dim][item[dim]] += 1
    return out


def shots_by_id(data):
    return {shot["id"]: shot for shot in data["shots"]}
