"""The pinned fallback selection: which open-licence photo stands in for which shot.

Stored as JSON (docs/team-shot-plan/fallback_selection.json) and also embedded in the
generated survey document between marker comments, so either file fixes the picks.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON = os.path.join(HERE, "fallback_selection.json")
DEFAULT_LOCK = os.path.join(HERE, "fallback_checksums.json")
DEFAULT_SURVEY_MD = os.path.join(os.path.dirname(HERE), "test-photo-set-survey.md")

MD_START = "<!-- fallback-selection:start -->"
MD_END = "<!-- fallback-selection:end -->"
PIN_FIELDS = ("slot", "source", "id", "page_url", "url", "title", "creator", "license",
              "license_url", "width", "height", "sha1", "attribution", "as_of")


class SelectionError(ValueError):
    pass


def embed_block(selection):
    body = json.dumps(selection, indent=2, sort_keys=True)
    return "%s\n```json\n%s\n```\n%s" % (MD_START, body, MD_END)


def _from_markdown(text):
    match = re.search(re.escape(MD_START) + r"\s*```json\n(.*?)\n```\s*" + re.escape(MD_END), text, re.S)
    if not match:
        raise SelectionError("no embedded fallback selection block found")
    return json.loads(match.group(1))


def load_selection(path):
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        data = _from_markdown(text) if path.endswith(".md") else json.loads(text)
    except OSError as exc:
        raise SelectionError("cannot read %s: %s" % (path, exc))
    except json.JSONDecodeError as exc:
        raise SelectionError("%s holds invalid JSON: %s" % (path, exc))
    validate_selection(data)
    return data


def validate_selection(data):
    pins = data.get("pins") if isinstance(data, dict) else None
    if not isinstance(pins, list):
        raise SelectionError("selection needs a 'pins' list")
    slots = set()
    for pin in pins:
        missing = [f for f in PIN_FIELDS if f not in pin]
        if missing:
            raise SelectionError("pin %s lacks fields: %s" % (pin.get("slot", "?"), ", ".join(missing)))
        if not str(pin["url"]).startswith("https://"):
            raise SelectionError("pin %s: url must be https" % pin["slot"])
        if pin["slot"] in slots:
            raise SelectionError("pin %s appears twice" % pin["slot"])
        slots.add(pin["slot"])


def find_existing():
    """Path of the first selection that exists and parses, preferring the JSON file."""
    for path in (DEFAULT_JSON, DEFAULT_SURVEY_MD):
        if os.path.isfile(path):
            try:
                load_selection(path)
                return path
            except SelectionError:
                continue
    return None
