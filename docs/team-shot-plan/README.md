# Team-shot photo plan

A plan to shoot 20 family-style photos ourselves, with a release for every
person shown, and to publish them as CC0.

| File | Purpose |
| --- | --- |
| `shot_list.json` | The 20 shots (subject, lighting, framing, example scene), target resolution, schedule |
| `RIGHTS.md` | Rights process and rules for children |
| `release_template.md` | Release to sign or record, with the manifest entry |
| `CC0-DEDICATION.md` | Commit-ready CC0 dedication |
| `validate_photos.py` | Validates a folder of submitted photos |
| `strip_metadata.py` | Lossless JPEG metadata stripper |
| `survey.py` | Surveys open sources as a fallback; writes `docs/test-photo-set-survey.md` |
| `fetch_fallback.py` | Downloads the pinned fallback photos and writes an attribution file |

Only the Python 3.9+ standard library is used.

## Submission folder

```
submission/
  manifest.json
  S01.jpg ... S20.jpg
  releases/R-001.pdf ...
```

`manifest.json`:

```json
{
  "releases": [
    {"id": "R-001", "type": "signed", "role": "adult", "file": "releases/R-001.pdf",
     "sha256": "<sha256>", "signed_on": "2025-06-01", "covers_cc0": true},
    {"id": "R-002", "type": "recorded", "role": "minor_by_guardian", "guardian_relationship": "parent",
     "file": "releases/R-002.m4a", "sha256": "<sha256>", "signed_on": "2025-06-01", "covers_cc0": true}
  ],
  "photos": [
    {"file": "S01.jpg", "shot_id": "S01", "photographer": "A. Photographer", "taken_on": "2025-06-06",
     "cc0_dedicated": true, "bystanders_identifiable": false,
     "people": [{"release_id": "R-002"}]}
  ]
}
```

An optional `"actual": {"subject": ..., "lighting": ..., "framing": ...}` on a photo
records that the shot ended up different from the plan; the mix check then counts
the actual labels.

## Commands

```
python docs/team-shot-plan/strip_metadata.py raw/*.jpg --out-dir submission
python docs/team-shot-plan/validate_photos.py submission            # exit 0 = valid
python docs/team-shot-plan/validate_photos.py submission --allow-partial   # mid-shoot check
python docs/team-shot-plan/survey.py                                # regenerate the survey
python docs/team-shot-plan/fetch_fallback.py                        # download fallback photos
python -m unittest discover -s tests
```
