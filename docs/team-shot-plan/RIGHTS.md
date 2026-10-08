# Rights process for the team-shot photo set

Goal: every committed photo can be reused by anyone (CC0) without a later claim
from a person shown in it.

## 1. Who needs a release

| Shown in the photo | Needed |
| --- | --- |
| Any identifiable adult | Own release (`role: adult`) |
| Any child under 18 | Release signed by a parent or legal guardian (`role: minor_by_guardian`) |
| Pets, objects, rooms | No release, but no visible addresses, number plates, screens with text, brands in focus, or artwork by others |
| Bystanders | Not allowed. Reshoot or crop so nobody unreleased is identifiable (`bystanders_identifiable: false`) |

Photographers also sign the CC0 dedication for their own work (`cc0_dedicated: true`).

## 2. Steps

1. Coordinator sends `release_template.md` to each household before the shoot.
2. Each adult signs, or records the spoken release; each guardian signs for their child.
3. Coordinator stores the scan or recording under `releases/`, computes its sha256
   (`sha256sum releases/R-001.pdf`) and adds it to `manifest.json`.
4. Photographer shoots, culls, uprights pixels, strips metadata
   (`strip_metadata.py`) and names files by shot id (`S01.jpg`).
5. Photographer adds each photo to `manifest.json` with the shot id, taken date,
   `people` (one `release_id` each) and `cc0_dedicated: true`.
6. `validate_photos.py <folder>` must report `RESULT: OK`.
7. A second person reads the manifest against the releases (rights review), then the
   folder is committed together with `CC0-DEDICATION.md` (filled in).

A release must be dated on or before the shoot day; the validator rejects later dates.

## 3. Rules for children

- Only the child's own parent or legal guardian signs. A friend, grandparent or
  teacher cannot, unless they hold legal guardianship.
- The child is told what the photo is for and may say no at any time; stop if they do.
  No payment or reward tied to being photographed.
- No names, school uniforms with names or crests, home or school exteriors,
  street signs, or location detail in frame or in file names.
- No swimwear, bath or bed-undressed scenes, no photos in bathrooms or bedrooms
  where a child is changing. Bedtime shot S13 is fully dressed, in pyjamas at most.
- Use only children whose household the team knows and can contact. Withdrawal
  before commit is honoured by deleting the photo and its manifest entry.
- Keep each guardian's contact details outside the repository; the manifest
  holds only release ids.

## 4. What never goes in the repository

Release scans contain names and signatures. In the repository keep the manifest and
the release ids only; hold the scans in a private store and give the validator a
local copy of the folder when it runs.
Open-source fallback photos are different: CC0 on a hosting site does not prove that the
people shown agreed. Treat those as unverified (see the survey document's rights risks).
