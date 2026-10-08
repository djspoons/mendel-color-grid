# Test photo set survey: team-shot photo plan

Approach: shoot the 20 photos ourselves from a shot list, with a release for everyone shown and a CC0 dedication; use open sources only as a fallback. Everything below the plan is produced by `docs/team-shot-plan/survey.py`; do not edit by hand.

## What was read

- As-of date (UTC): **2026-10-08**
- Local: `docs/team-shot-plan/shot_list.json` (20 shots)
- Sources visited: Wikimedia Commons (MediaWiki API), Openverse (API). Routes and counts:

| Source | Route | Request | Count |
| --- | --- | --- | --- |
| Wikimedia Commons | search API (incategory:CC-Zero filetype:bitmap) | list=search | 8465823 |
| Wikimedia Commons | category page (Category:CC-Zero) | prop=categoryinfo | 9875348 files, 14 subcategories |
| Wikimedia Commons | search API, query 'family' | list=search | 298819 |
| Openverse | stats endpoint (all licences, 52 providers) | /images/stats/ | 0 images; largest: wikimedia 0, animaldiversity 0, bio_diversity 0, brooklynmuseum 0 |
| Openverse | search API, license=cc0, q=family | /images/ | 240 |
| Openverse | search API, license=pdm, q=family | /images/ | 240 |
| Both | per-shot search, 20 shots x 2 sources | see Coverage mix | 0 of 40 queries failed or were skipped |

**Run status: not everything was read as planned.**

- Openverse was read anonymously (no OPENVERSE_CLIENT_ID/SECRET set); its anonymous rate limit may stop some per-shot queries.
- FAILED READ (suspect): an Openverse count is under 1000 where thousands are expected.

Selection: chosen in this run and pinned below.

Where the two Commons routes disagree (search hits vs category files) that is a finding: the search also reaches files in CC-Zero subcategories and matches by text, the category count covers direct members only.

## Candidate sources

| Source | Licence | Commit and reuse clearly allowed? | Attribution | Scriptable fetch | Rights flag |
| --- | --- | --- | --- | --- | --- |
| Team-shot photos (this plan) | CC0 1.0 dedication by us, plus releases | Yes, we own the rights and hold releases | None required | Not needed; `validate_photos.py` checks the folder | None once releases validate |
| Wikimedia Commons, CC-Zero files | CC0 1.0 as declared by the uploader | Yes for the copyright; uploader's claim not verified | None required (courtesy credit recorded) | Yes, API keyless, descriptive User-Agent needed, SHA-1 published | Unclear for identifiable people: CC0 does not cover personality rights |
| Openverse, licence filter cc0 / pdm | CC0 1.0 or Public Domain Mark 1.0, as passed on from the provider | CC0 yes; Public Domain Mark is a label, not a waiver, so check the provider | None required (courtesy credit recorded) | Yes, API; anonymous limits are tight, optional OAuth lifts them; no checksum | Unclear for identifiable people; aggregator, so the provider's own terms are the source of truth |
| Unsplash, Pexels, Pixabay | Each site's own licence, not CC0 | Not clearly: those licences limit redistributing the photos as a set | Not required, but terms vary | API keys needed; not read in this run | Rights unclear for committing a copy; model releases not guaranteed |

The last row comes from those sites' published licence terms and was not machine-checked in this run.

## Recommended set

Recommended: the team-shot set below. The photos do not exist yet, so the ID/URL column is the path each photo takes in the submission folder. Resolution: minimum 2400x1600 px (long x short edge), target 4000x3000 px, jpg/jpeg/png.

| Slot | ID/URL | Creator | License | Attribution string | Subject | Lighting | Framing | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | photos/S01.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | single_child | indoor | close-up | >=2400x1600, target 4000x3000 |
| S02 | photos/S02.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | single_child | bright | medium | >=2400x1600, target 4000x3000 |
| S03 | photos/S03.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | single_child | backlit | wide | >=2400x1600, target 4000x3000 |
| S04 | photos/S04.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | single_child | low_light | close-up | >=2400x1600, target 4000x3000 |
| S05 | photos/S05.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | single_child | bright | close-up | >=2400x1600, target 4000x3000 |
| S06 | photos/S06.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | group | bright | wide | >=2400x1600, target 4000x3000 |
| S07 | photos/S07.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | group | indoor | medium | >=2400x1600, target 4000x3000 |
| S08 | photos/S08.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | group | low_light | wide | >=2400x1600, target 4000x3000 |
| S09 | photos/S09.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | group | backlit | medium | >=2400x1600, target 4000x3000 |
| S10 | photos/S10.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | adults_with_children | indoor | close-up | >=2400x1600, target 4000x3000 |
| S11 | photos/S11.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | adults_with_children | bright | medium | >=2400x1600, target 4000x3000 |
| S12 | photos/S12.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | adults_with_children | indoor | wide | >=2400x1600, target 4000x3000 |
| S13 | photos/S13.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | adults_with_children | low_light | medium | >=2400x1600, target 4000x3000 |
| S14 | photos/S14.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | adults_with_children | backlit | close-up | >=2400x1600, target 4000x3000 |
| S15 | photos/S15.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | pets | bright | medium | >=2400x1600, target 4000x3000 |
| S16 | photos/S16.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | pets | indoor | close-up | >=2400x1600, target 4000x3000 |
| S17 | photos/S17.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | pets | backlit | wide | >=2400x1600, target 4000x3000 |
| S18 | photos/S18.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | objects | indoor | medium | >=2400x1600, target 4000x3000 |
| S19 | photos/S19.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | objects | bright | wide | >=2400x1600, target 4000x3000 |
| S20 | photos/S20.jpg (to be shot) | team photographer, named in manifest.json | CC0 1.0 (CC0-DEDICATION.md + releases) | None required | objects | low_light | close-up | >=2400x1600, target 4000x3000 |

Example scenes:

- **S01** (single_child, indoor, close-up; 1 people, 1 children): Child drawing at the kitchen table, face lit by window light, pencil in hand.
- **S02** (single_child, bright, medium; 1 people, 1 children): Child riding a bicycle on the driveway in midday sun, helmet on, knees up to head in frame.
- **S03** (single_child, backlit, wide; 1 people, 1 children): Child running through a garden sprinkler with low sun behind, spray catching the light.
- **S04** (single_child, low_light, close-up; 1 people, 1 children): Child reading under a blanket by torch light, face softly lit.
- **S05** (single_child, bright, close-up; 1 people, 1 children): Child blowing bubbles in the garden, open shade, bubbles in focus range.
- **S06** (group, bright, wide; 5 people, 2 children): Five people at a picnic blanket in a park, whole group and the setting visible.
- **S07** (group, indoor, medium; 4 people, 2 children): Four people playing a board game around a table under ceiling light.
- **S08** (group, low_light, wide; 4 people, 2 children): Family on a sofa for movie night, screen glow and one lamp as the only light.
- **S09** (group, backlit, medium; 4 people, 2 children): Family walking along a beach at golden hour with the sun behind them.
- **S10** (adults_with_children, indoor, close-up; 2 people, 1 children): Parent reading a picture book to a child, both faces in frame.
- **S11** (adults_with_children, bright, medium; 2 people, 1 children): Parent pushing a child on a playground swing in full daylight.
- **S12** (adults_with_children, indoor, wide; 3 people, 1 children): Two adults and a child tidying a living room, whole room visible.
- **S13** (adults_with_children, low_light, medium; 2 people, 1 children): Bedtime story: adult sitting on the edge of a child's bed, bedside lamp only.
- **S14** (adults_with_children, backlit, close-up; 2 people, 1 children): Adult lifting a laughing child against a bright window or low sun, rim light on hair.
- **S15** (pets, bright, medium; 0 people, 0 children): Dog sitting on a lawn in daylight, looking at the camera.
- **S16** (pets, indoor, close-up; 0 people, 0 children): Cat curled on a sofa or windowsill, face and paws in frame.
- **S17** (pets, backlit, wide; 0 people, 0 children): Dog on a hillside or field at sunset, sun behind, landscape visible.
- **S18** (objects, indoor, medium; 0 people, 0 children): School bag, shoes and coats by the front door in the hallway.
- **S19** (objects, bright, wide; 0 people, 0 children): Back garden with table, chairs and scattered toys, nobody in frame.
- **S20** (objects, low_light, close-up; 0 people, 0 children): Birthday cake with lit candles on a table in a dim room, no faces.

### Fallback pins from open sources

Use only if team photos are late. Subject, lighting and framing are what the shot slot asks for, matched by keyword search; they were **not** checked by eye. `fetch_fallback.py` downloads exactly these pins.

| Slot | Source | ID | URL | Creator | License | Attribution string | Resolution | As of |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | wikimedia-commons | File:Drawing of a mother and child by Pablo O'Higgins.jpg (pageid 110879857) | https://upload.wikimedia.org/wikipedia/commons/a/a5/Drawing_of_a_mother_and_child_by_Pablo_O%27Higgins.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Pablo O'Higgins | CC0 | Drawing of a mother and child by Pablo O'Higgins by Pablo O'Higgins (https://commons.wikimedia.org/wiki/File:Drawing_of_a_mother_and_child_by_Pablo_O%27Higgins.jpg), CC0 | 5472x7296 | 2026-10-08 |
| S02 | wikimedia-commons | File:Rental bicycle child carrier at Tourism Office in Trégastel.jpg (pageid 177355556) | https://upload.wikimedia.org/wikipedia/commons/4/46/Rental_bicycle_child_carrier_at_Tourism_Office_in_Tr%C3%A9gastel.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Syced | CC0 | Rental bicycle child carrier at Tourism Office in Trégastel by Syced (https://commons.wikimedia.org/wiki/File:Rental_bicycle_child_carrier_at_Tourism_Office_in_Tr%C3%A9gastel.jpg), CC0 | 4080x3072 | 2026-10-08 |
| S03 | openverse | 556c9570-8cca-4d45-a7d6-ac04396f40f8 | https://cdn.stocksnap.io/img-thumbs/960w/VZ66NHFPRR.jpg | frank mckenna | CC0 1.0 | Kids Child by frank mckenna (https://stocksnap.io/photo/kids-child-VZ66NHFPRR), CC0 1.0 | 4928x3280 | 2026-10-08 |
| S04 | openverse | 1ecec18f-4818-4a9d-890a-8d4f8d1abe41 | https://cdn.stocksnap.io/img-thumbs/960w/EKUBIBCEOF.jpg | Direct Media | CC0 1.0 | Father Son by Direct Media (https://stocksnap.io/photo/father-son-EKUBIBCEOF), CC0 1.0 | 8688x5792 | 2026-10-08 |
| S05 | wikimedia-commons | File:Frozen soap bubble behind fir twigs (Unsplash BojuZpqw4zM).jpg (pageid 62202478) | https://upload.wikimedia.org/wikipedia/commons/9/93/Frozen_soap_bubble_behind_fir_twigs_%28Unsplash_BojuZpqw4zM%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | aaronburden Aaron Burden from Baltimore, Maryland, USA. | CC0 | Frozen soap bubble behind fir twigs (Unsplash BojuZpqw4zM) by aaronburden Aaron Burden from Baltimore, Maryland, USA. (https://commons.wikimedia.org/wiki/File:Frozen_soap_bubble_behind_fir_twigs_(Unsplash_BojuZpqw4zM).jpg), CC0 | 4608x3456 | 2026-10-08 |
| S06 | wikimedia-commons | File:Family picnic, Himeji Castle grounds, Himeji, 2016.jpg (pageid 154099397) | https://upload.wikimedia.org/wikipedia/commons/0/0f/Family_picnic%2C_Himeji_Castle_grounds%2C_Himeji%2C_2016.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | DimiTalen | CC0 | Family picnic, Himeji Castle grounds, Himeji, 2016 by DimiTalen (https://commons.wikimedia.org/wiki/File:Family_picnic,_Himeji_Castle_grounds,_Himeji,_2016.jpg), CC0 | 3109x4676 | 2026-10-08 |
| S07 | wikimedia-commons | File:Loteria de Animalitos (Oriente de Venezuela).png (pageid 168147571) | https://upload.wikimedia.org/wikipedia/commons/5/51/Loteria_de_Animalitos_%28Oriente_de_Venezuela%29.png?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Jlannons99 | CC0 | Loteria de Animalitos (Oriente de Venezuela) by Jlannons99 (https://commons.wikimedia.org/wiki/File:Loteria_de_Animalitos_(Oriente_de_Venezuela).png), CC0 | 3581x5148 | 2026-10-08 |
| S09 | wikimedia-commons | File:Family watching beach sunset (Unsplash).jpg (pageid 61705751) | https://upload.wikimedia.org/wikipedia/commons/d/de/Family_watching_beach_sunset_%28Unsplash%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | David Straight davidstraight | CC0 | Family watching beach sunset (Unsplash) by David Straight davidstraight (https://commons.wikimedia.org/wiki/File:Family_watching_beach_sunset_(Unsplash).jpg), CC0 | 4608x3072 | 2026-10-08 |
| S10 | wikimedia-commons | File:Moeder leest haar kind voor uit een boek, RP-P-OB-70.588.jpg (pageid 148196338) | https://upload.wikimedia.org/wikipedia/commons/5/57/Moeder_leest_haar_kind_voor_uit_een_boek%2C_RP-P-OB-70.588.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Rijksmuseum | CC0 | Moeder leest haar kind voor uit een boek, RP-P-OB-70.588 by Rijksmuseum (https://commons.wikimedia.org/wiki/File:Moeder_leest_haar_kind_voor_uit_een_boek,_RP-P-OB-70.588.jpg), CC0 | 4998x6372 | 2026-10-08 |
| S11 | openverse | e4d976b1-b2f5-476e-a56f-da4bd37162a9 | https://cdn.stocksnap.io/img-thumbs/960w/NU8CU1E2AK.jpg | Family Moments | CC0 1.0 | Playground Child by Family Moments (https://stocksnap.io/photo/playground-child-NU8CU1E2AK), CC0 1.0 | 5760x3840 | 2026-10-08 |
| S12 | wikimedia-commons | File:Familien Waagepetersen 1830 by Wilhelm Bendz.jpg (pageid 19146634) | https://upload.wikimedia.org/wikipedia/commons/3/36/Familien_Waagepetersen_1830_by_Wilhelm_Bendz.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Wilhelm Bendz | CC0 | Familien Waagepetersen 1830 by Wilhelm Bendz by Wilhelm Bendz (https://commons.wikimedia.org/wiki/File:Familien_Waagepetersen_1830_by_Wilhelm_Bendz.jpg), CC0 | 6563x7463 | 2026-10-08 |
| S13 | wikimedia-commons | File:Bedtime stories (Unsplash).jpg (pageid 62146030) | https://upload.wikimedia.org/wikipedia/commons/6/64/Bedtime_stories_%28Unsplash%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Vibhav Kapoor vibhavkapoor | CC0 | Bedtime stories (Unsplash) by Vibhav Kapoor vibhavkapoor (https://commons.wikimedia.org/wiki/File:Bedtime_stories_(Unsplash).jpg), CC0 | 5944x3962 | 2026-10-08 |
| S14 | openverse | 1d11d8a1-26eb-446a-b6c2-89fbec545886 | https://cdn.stocksnap.io/img-thumbs/960w/SA3W6QFGIM.jpg | Salvatore Ventura | CC0 1.0 | Sunset Golden by Salvatore Ventura (https://stocksnap.io/photo/sunset-golden-SA3W6QFGIM), CC0 1.0 | 6016x4016 | 2026-10-08 |
| S15 | wikimedia-commons | File:Garden ceramic dog Auchan Mikołów.jpg (pageid 178433528) | https://upload.wikimedia.org/wikipedia/commons/5/56/Garden_ceramic_dog_Auchan_Miko%C5%82%C3%B3w.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Abraham | CC0 | Garden ceramic dog Auchan Mikołów by Abraham (https://commons.wikimedia.org/wiki/File:Garden_ceramic_dog_Auchan_Miko%C5%82%C3%B3w.jpg), CC0 | 3000x4000 | 2026-10-08 |
| S16 | wikimedia-commons | File:Cat staring out window (2023-08-14).jpg (pageid 135941066) | https://upload.wikimedia.org/wikipedia/commons/8/85/Cat_staring_out_window_%282023-08-14%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Roc0ast3r | CC0 | Cat staring out window (2023-08-14) by Roc0ast3r (https://commons.wikimedia.org/wiki/File:Cat_staring_out_window_(2023-08-14).jpg), CC0 | 3864x5152 | 2026-10-08 |
| S17 | wikimedia-commons | File:Playtime at sunset. ( Explored ) - Flickr - Oneterry AKA Terry Kearney.jpg (pageid 176630081) | https://upload.wikimedia.org/wikipedia/commons/9/94/Playtime_at_sunset._%28_Explored_%29_-_Flickr_-_Oneterry_AKA_Terry_Kearney.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Terry Kearney from liverpool, merseyside | CC0 | Playtime at sunset. ( Explored ) - Flickr - Oneterry AKA Terry Kearney by Terry Kearney from liverpool, merseyside (https://commons.wikimedia.org/wiki/File:Playtime_at_sunset._(_Explored_)_-_Flickr_-_Oneterry_AKA_Terry_Kearney.jpg), CC0 | 4352x3264 | 2026-10-08 |
| S20 | wikimedia-commons | File:Tim Tams and Nuts on a Birthday Cake With Candles during her Anniversary.jpg (pageid 191012522) | https://upload.wikimedia.org/wikipedia/commons/d/d1/Tim_Tams_and_Nuts_on_a_Birthday_Cake_With_Candles_during_her_Anniversary.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Brassluff | CC0 | Tim Tams and Nuts on a Birthday Cake With Candles during her Anniversary by Brassluff (https://commons.wikimedia.org/wiki/File:Tim_Tams_and_Nuts_on_a_Birthday_Cake_With_Candles_during_her_Anniversary.jpg), CC0 | 3024x4032 | 2026-10-08 |

## Coverage mix

Team-shot plan (all 20 shots, counts from the shot list):

| Dimension | Counts |
| --- | --- |
| Subject | single_child 5, group 4, adults_with_children 5, pets 3, objects 3 |
| Lighting | bright 6, indoor 6, low_light 4, backlit 4 |
| Framing | close-up 7, medium 7, wide 6 |

Gaps left in the plan (subject by lighting), each for the same reason: the 20-shot budget keeps one or two shots per combination, and these combinations were dropped first because they are the hardest to shoot safely or the least typical of family photos:

- pets has no low_light shot
- objects has no backlit shot

Fallback pins (17 of 20 slots filled):

| Dimension | Counts |
| --- | --- |
| Subject | single_child 5, group 3, adults_with_children 5, pets 3, objects 1 |
| Lighting | bright 5, indoor 5, low_light 3, backlit 4 |
| Framing | close-up 7, medium 6, wide 4 |

Slots with no fallback pin, and why:

- S08 (group, low_light, wide): commons: 0 returned, 0 passed licence/size; openverse: 20 returned, 0 passed licence/size
- S18 (objects, indoor, medium): commons: 0 returned, 0 passed licence/size; openverse: 0 returned, 0 passed licence/size
- S19 (objects, bright, wide): commons: 0 returned, 0 passed licence/size; openverse: 0 returned, 0 passed licence/size

Per-slot candidates found by search (hits = total matches the source reports; qualifying = licence, size and file type pass, out of the first page returned):

| Slot | Query | Commons | Openverse | Pinned from |
| --- | --- | --- | --- | --- |
| S01 | child drawing | 3829 hits, 18/29 qualifying | 240 hits, 6/20 qualifying | wikimedia-commons |
| S02 | child bicycle | 42 hits, 26/30 qualifying | 10 hits, 4/10 qualifying | wikimedia-commons |
| S03 | child sprinkler | 0 hits, 0/0 qualifying | 2 hits, 2/2 qualifying | openverse |
| S04 | child reading flashlight | 0 hits, 0/0 qualifying | 9 hits, 9/9 qualifying | openverse |
| S05 | child bubbles | 891 hits, 19/30 qualifying | 16 hits, 11/16 qualifying | wikimedia-commons |
| S06 | family picnic | 130 hits, 17/30 qualifying | 240 hits, 0/20 qualifying | wikimedia-commons |
| S07 | family board game | 10 hits, 2/9 qualifying | 4 hits, 3/4 qualifying | wikimedia-commons |
| S08 | family movie night | 0 hits, 0/0 qualifying | 118 hits, 0/20 qualifying | none |
| S09 | family beach sunset | 5 hits, 3/5 qualifying | 1 hits, 1/1 qualifying | wikimedia-commons |
| S10 | mother child reading | 4 hits, 1/3 qualifying | 239 hits, 13/20 qualifying | wikimedia-commons |
| S11 | father child swing | 0 hits, 0/0 qualifying | 9 hits, 9/9 qualifying | openverse |
| S12 | family living room | 50 hits, 27/29 qualifying | 99 hits, 1/20 qualifying | wikimedia-commons |
| S13 | bedtime story | 4 hits, 1/4 qualifying | 5 hits, 3/5 qualifying | wikimedia-commons |
| S14 | parent child sunset | 0 hits, 0/0 qualifying | 2 hits, 1/2 qualifying | openverse |
| S15 | dog garden | 887 hits, 22/25 qualifying | 216 hits, 0/20 qualifying | wikimedia-commons |
| S16 | cat window | 2429 hits, 19/30 qualifying | 58 hits, 8/20 qualifying | wikimedia-commons |
| S17 | dog sunset field | 3 hits, 3/3 qualifying | 1 hits, 0/1 qualifying | wikimedia-commons |
| S18 | school bag shoes hallway | 0 hits, 0/0 qualifying | 0 hits, 0/0 qualifying | none |
| S19 | garden table toys | 0 hits, 0/0 qualifying | 0 hits, 0/0 qualifying | none |
| S20 | birthday cake candles | 23 hits, 19/23 qualifying | 49 hits, 12/20 qualifying | wikimedia-commons |

## Rights risks

- Identifiable children: 14 of the 20 planned shots show children. With our own photos every child has a release signed by a parent or guardian (`RIGHTS.md`); `validate_photos.py` fails a photo without one.
- Open-source fallback: CC0 or public domain covers copyright only. It says nothing about a model release for the people shown. 13 fallback pins are planned to show people (S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14) and 13 of those show children (S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14); none has a verified release. Avoid committing these; prefer slots with pets or objects, or reshoot.
- Uploader claims: a CC0 label on Commons or Openverse is the uploader's statement and may be wrong (someone else's photo). Pins that rely on it have not been independently verified.
- Public Domain Mark (Openverse `pdm`) is a label, not a legal waiver: prefer CC0 when both exist.
- Avoid: photos with a Commons `Restrictions` note (these are filtered out), minors in swimwear or private spaces, readable names, addresses, number plates, school crests, and any source licence that limits redistribution (Unsplash, Pexels, Pixabay terms).
- Release scans hold names and signatures; keep them out of the repository and commit only release ids and checksums.

## Cost and schedule

| Step | Who | Hours | Calendar |
| --- | --- | --- | --- |
| Recruit two or three households, agree dates, send release pack | coordinator | 3.0 | days 1-3 |
| Collect signed or recorded releases (adults, guardians for children), file with sha256 | coordinator | 2.0 | days 3-5 |
| Session A: indoor and window light (S01, S07, S10, S12, S16, S18) | photographer | 2.5 | day 6 |
| Session B: bright daylight outdoors (S02, S05, S06, S11, S15, S19) | photographer | 2.5 | day 6 or 7 |
| Session C: golden hour, backlit (S03, S09, S14, S17) | photographer | 1.5 | day 7 |
| Session D: evening low light (S04, S08, S13, S20) | photographer | 1.5 | day 7 or 8 |
| Cull, upright, strip metadata, name files by shot id | photographer | 3.0 | day 8 |
| Run validate_photos.py, fix findings, reshoot any failed shot (allowance) | photographer | 3.0 | days 9-10 |
| Rights review of manifest and releases, commit with CC0 dedication | coordinator | 2.0 | day 10 |

Total effort: **21.0 person-hours** over about 10 calendar days (shoots fit into two weekend-style days because the golden-hour and evening sessions depend on daylight). Cash cost: no licence fees; phone cameras suffice; household volunteers are unpaid, as the release says. The 3 hours of validation and reshoot time is an allowance, not a measured figure. For comparison, the fallback is scripted (minutes to download) but needs a manual look at 20 pins and still leaves unverified rights, so it cannot replace the team shoot for people photos.

## Fetch script

- Team photos: they do not exist yet, so no script can download them. This variation cannot produce that part. Check a submitted folder with `python docs/team-shot-plan/validate_photos.py <folder>` (resolution, metadata stripped, release trail, shot ids, mix counts); strip metadata with `strip_metadata.py`.
- Fallback photos: `python docs/team-shot-plan/fetch_fallback.py` downloads the 17 pinned photos to `photos/fallback/` and writes `photos/fallback/ATTRIBUTION.txt`. It uses the standard library only, retries network errors, writes atomically, skips files that already verify (idempotent), checks JPEG/PNG header, minimum resolution, the pinned SHA-1 (Commons pins) and a SHA-256 lock recorded on first download in `fallback_checksums.json` (Openverse pins have no source checksum, so they are trusted on first download), reports failed slots and exits 1 if any failed. Pins read from `fallback_selection.json` or the block at the end of this document.
- Slots without a pin (S08, S18, S19) have nothing to download.

## Open questions

- Round 1: Which two or three households can we recruit, and who acts as coordinator for the releases?
- Round 1: Is the 2400x1600 minimum acceptable, or does the consuming test need larger originals?
- Round 2: Should fallback pins of people be allowed at all, given no release can be verified?
- Round 2: Where do release scans live (private store), and who does the rights review?
- Round 3: Are the dropped subject/lighting combinations acceptable, or should a second batch cover them?
- Round 3: Should the fallback pins be eyeballed (subject, lighting, framing) before anyone relies on them?

## Pinned fallback selection (machine-readable)

<!-- fallback-selection:start -->
```json
{
  "as_of": "2026-10-08",
  "pins": [
    {
      "as_of": "2026-10-08",
      "attribution": "Drawing of a mother and child by Pablo O'Higgins by Pablo O'Higgins (https://commons.wikimedia.org/wiki/File:Drawing_of_a_mother_and_child_by_Pablo_O%27Higgins.jpg), CC0",
      "creator": "Pablo O'Higgins",
      "height": 7296,
      "id": "File:Drawing of a mother and child by Pablo O'Higgins.jpg (pageid 110879857)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Drawing_of_a_mother_and_child_by_Pablo_O%27Higgins.jpg",
      "sha1": "2861154a5be149ae189d50aa27056790c2143420",
      "slot": "S01",
      "source": "wikimedia-commons",
      "title": "Drawing of a mother and child by Pablo O'Higgins",
      "url": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Drawing_of_a_mother_and_child_by_Pablo_O%27Higgins.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 5472
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Rental bicycle child carrier at Tourism Office in Tr\u00e9gastel by Syced (https://commons.wikimedia.org/wiki/File:Rental_bicycle_child_carrier_at_Tourism_Office_in_Tr%C3%A9gastel.jpg), CC0",
      "creator": "Syced",
      "height": 3072,
      "id": "File:Rental bicycle child carrier at Tourism Office in Tr\u00e9gastel.jpg (pageid 177355556)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Rental_bicycle_child_carrier_at_Tourism_Office_in_Tr%C3%A9gastel.jpg",
      "sha1": "6cbccd37caf40d41eca1a0b971826e0a5ca589f8",
      "slot": "S02",
      "source": "wikimedia-commons",
      "title": "Rental bicycle child carrier at Tourism Office in Tr\u00e9gastel",
      "url": "https://upload.wikimedia.org/wikipedia/commons/4/46/Rental_bicycle_child_carrier_at_Tourism_Office_in_Tr%C3%A9gastel.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 4080
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Kids Child by frank mckenna (https://stocksnap.io/photo/kids-child-VZ66NHFPRR), CC0 1.0",
      "creator": "frank mckenna",
      "height": 3280,
      "id": "556c9570-8cca-4d45-a7d6-ac04396f40f8",
      "license": "CC0 1.0",
      "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
      "page_url": "https://stocksnap.io/photo/kids-child-VZ66NHFPRR",
      "sha1": null,
      "slot": "S03",
      "source": "openverse",
      "title": "Kids Child",
      "url": "https://cdn.stocksnap.io/img-thumbs/960w/VZ66NHFPRR.jpg",
      "width": 4928
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Father Son by Direct Media (https://stocksnap.io/photo/father-son-EKUBIBCEOF), CC0 1.0",
      "creator": "Direct Media",
      "height": 5792,
      "id": "1ecec18f-4818-4a9d-890a-8d4f8d1abe41",
      "license": "CC0 1.0",
      "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
      "page_url": "https://stocksnap.io/photo/father-son-EKUBIBCEOF",
      "sha1": null,
      "slot": "S04",
      "source": "openverse",
      "title": "Father Son",
      "url": "https://cdn.stocksnap.io/img-thumbs/960w/EKUBIBCEOF.jpg",
      "width": 8688
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Frozen soap bubble behind fir twigs (Unsplash BojuZpqw4zM) by aaronburden Aaron Burden from Baltimore, Maryland, USA. (https://commons.wikimedia.org/wiki/File:Frozen_soap_bubble_behind_fir_twigs_(Unsplash_BojuZpqw4zM).jpg), CC0",
      "creator": "aaronburden Aaron Burden from Baltimore, Maryland, USA.",
      "height": 3456,
      "id": "File:Frozen soap bubble behind fir twigs (Unsplash BojuZpqw4zM).jpg (pageid 62202478)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Frozen_soap_bubble_behind_fir_twigs_(Unsplash_BojuZpqw4zM).jpg",
      "sha1": "89d7d59cf545b3268ab0b050cd1b68747647878c",
      "slot": "S05",
      "source": "wikimedia-commons",
      "title": "Frozen soap bubble behind fir twigs (Unsplash BojuZpqw4zM)",
      "url": "https://upload.wikimedia.org/wikipedia/commons/9/93/Frozen_soap_bubble_behind_fir_twigs_%28Unsplash_BojuZpqw4zM%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 4608
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Family picnic, Himeji Castle grounds, Himeji, 2016 by DimiTalen (https://commons.wikimedia.org/wiki/File:Family_picnic,_Himeji_Castle_grounds,_Himeji,_2016.jpg), CC0",
      "creator": "DimiTalen",
      "height": 4676,
      "id": "File:Family picnic, Himeji Castle grounds, Himeji, 2016.jpg (pageid 154099397)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Family_picnic,_Himeji_Castle_grounds,_Himeji,_2016.jpg",
      "sha1": "0e154c160f4d53e05b00527dc455f174ead2ea1d",
      "slot": "S06",
      "source": "wikimedia-commons",
      "title": "Family picnic, Himeji Castle grounds, Himeji, 2016",
      "url": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Family_picnic%2C_Himeji_Castle_grounds%2C_Himeji%2C_2016.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 3109
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Loteria de Animalitos (Oriente de Venezuela) by Jlannons99 (https://commons.wikimedia.org/wiki/File:Loteria_de_Animalitos_(Oriente_de_Venezuela).png), CC0",
      "creator": "Jlannons99",
      "height": 5148,
      "id": "File:Loteria de Animalitos (Oriente de Venezuela).png (pageid 168147571)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Loteria_de_Animalitos_(Oriente_de_Venezuela).png",
      "sha1": "29f24ec3d7255e146286ad21a08142b86b9b8a15",
      "slot": "S07",
      "source": "wikimedia-commons",
      "title": "Loteria de Animalitos (Oriente de Venezuela)",
      "url": "https://upload.wikimedia.org/wikipedia/commons/5/51/Loteria_de_Animalitos_%28Oriente_de_Venezuela%29.png?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 3581
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Family watching beach sunset (Unsplash) by David Straight davidstraight (https://commons.wikimedia.org/wiki/File:Family_watching_beach_sunset_(Unsplash).jpg), CC0",
      "creator": "David Straight davidstraight",
      "height": 3072,
      "id": "File:Family watching beach sunset (Unsplash).jpg (pageid 61705751)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Family_watching_beach_sunset_(Unsplash).jpg",
      "sha1": "44e8dbfc327aa076a26b1d0ad7839e5bbdf0873e",
      "slot": "S09",
      "source": "wikimedia-commons",
      "title": "Family watching beach sunset (Unsplash)",
      "url": "https://upload.wikimedia.org/wikipedia/commons/d/de/Family_watching_beach_sunset_%28Unsplash%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 4608
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Moeder leest haar kind voor uit een boek, RP-P-OB-70.588 by Rijksmuseum (https://commons.wikimedia.org/wiki/File:Moeder_leest_haar_kind_voor_uit_een_boek,_RP-P-OB-70.588.jpg), CC0",
      "creator": "Rijksmuseum",
      "height": 6372,
      "id": "File:Moeder leest haar kind voor uit een boek, RP-P-OB-70.588.jpg (pageid 148196338)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Moeder_leest_haar_kind_voor_uit_een_boek,_RP-P-OB-70.588.jpg",
      "sha1": "561f3025a2b30543d90b1a78c7d5d7e65e40be87",
      "slot": "S10",
      "source": "wikimedia-commons",
      "title": "Moeder leest haar kind voor uit een boek, RP-P-OB-70.588",
      "url": "https://upload.wikimedia.org/wikipedia/commons/5/57/Moeder_leest_haar_kind_voor_uit_een_boek%2C_RP-P-OB-70.588.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 4998
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Playground Child by Family Moments (https://stocksnap.io/photo/playground-child-NU8CU1E2AK), CC0 1.0",
      "creator": "Family Moments",
      "height": 3840,
      "id": "e4d976b1-b2f5-476e-a56f-da4bd37162a9",
      "license": "CC0 1.0",
      "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
      "page_url": "https://stocksnap.io/photo/playground-child-NU8CU1E2AK",
      "sha1": null,
      "slot": "S11",
      "source": "openverse",
      "title": "Playground Child",
      "url": "https://cdn.stocksnap.io/img-thumbs/960w/NU8CU1E2AK.jpg",
      "width": 5760
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Familien Waagepetersen 1830 by Wilhelm Bendz by Wilhelm Bendz (https://commons.wikimedia.org/wiki/File:Familien_Waagepetersen_1830_by_Wilhelm_Bendz.jpg), CC0",
      "creator": "Wilhelm Bendz",
      "height": 7463,
      "id": "File:Familien Waagepetersen 1830 by Wilhelm Bendz.jpg (pageid 19146634)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Familien_Waagepetersen_1830_by_Wilhelm_Bendz.jpg",
      "sha1": "7db3587312c51540ae9fe84d25423cd474b79b2f",
      "slot": "S12",
      "source": "wikimedia-commons",
      "title": "Familien Waagepetersen 1830 by Wilhelm Bendz",
      "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Familien_Waagepetersen_1830_by_Wilhelm_Bendz.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 6563
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Bedtime stories (Unsplash) by Vibhav Kapoor vibhavkapoor (https://commons.wikimedia.org/wiki/File:Bedtime_stories_(Unsplash).jpg), CC0",
      "creator": "Vibhav Kapoor vibhavkapoor",
      "height": 3962,
      "id": "File:Bedtime stories (Unsplash).jpg (pageid 62146030)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Bedtime_stories_(Unsplash).jpg",
      "sha1": "56b7d39451c35c4dd5b71ccc6c4db6b59bfc5b7e",
      "slot": "S13",
      "source": "wikimedia-commons",
      "title": "Bedtime stories (Unsplash)",
      "url": "https://upload.wikimedia.org/wikipedia/commons/6/64/Bedtime_stories_%28Unsplash%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 5944
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Sunset Golden by Salvatore Ventura (https://stocksnap.io/photo/sunset-golden-SA3W6QFGIM), CC0 1.0",
      "creator": "Salvatore Ventura",
      "height": 4016,
      "id": "1d11d8a1-26eb-446a-b6c2-89fbec545886",
      "license": "CC0 1.0",
      "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
      "page_url": "https://stocksnap.io/photo/sunset-golden-SA3W6QFGIM",
      "sha1": null,
      "slot": "S14",
      "source": "openverse",
      "title": "Sunset Golden",
      "url": "https://cdn.stocksnap.io/img-thumbs/960w/SA3W6QFGIM.jpg",
      "width": 6016
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Garden ceramic dog Auchan Miko\u0142\u00f3w by Abraham (https://commons.wikimedia.org/wiki/File:Garden_ceramic_dog_Auchan_Miko%C5%82%C3%B3w.jpg), CC0",
      "creator": "Abraham",
      "height": 4000,
      "id": "File:Garden ceramic dog Auchan Miko\u0142\u00f3w.jpg (pageid 178433528)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Garden_ceramic_dog_Auchan_Miko%C5%82%C3%B3w.jpg",
      "sha1": "ab2f3df533fd024e20489e68461c19a01b7ec4dd",
      "slot": "S15",
      "source": "wikimedia-commons",
      "title": "Garden ceramic dog Auchan Miko\u0142\u00f3w",
      "url": "https://upload.wikimedia.org/wikipedia/commons/5/56/Garden_ceramic_dog_Auchan_Miko%C5%82%C3%B3w.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 3000
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Cat staring out window (2023-08-14) by Roc0ast3r (https://commons.wikimedia.org/wiki/File:Cat_staring_out_window_(2023-08-14).jpg), CC0",
      "creator": "Roc0ast3r",
      "height": 5152,
      "id": "File:Cat staring out window (2023-08-14).jpg (pageid 135941066)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Cat_staring_out_window_(2023-08-14).jpg",
      "sha1": "f4e5b8770780ca21df95cfffc0653e6dddd40994",
      "slot": "S16",
      "source": "wikimedia-commons",
      "title": "Cat staring out window (2023-08-14)",
      "url": "https://upload.wikimedia.org/wikipedia/commons/8/85/Cat_staring_out_window_%282023-08-14%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 3864
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Playtime at sunset. ( Explored ) - Flickr - Oneterry AKA Terry Kearney by Terry Kearney from liverpool, merseyside (https://commons.wikimedia.org/wiki/File:Playtime_at_sunset._(_Explored_)_-_Flickr_-_Oneterry_AKA_Terry_Kearney.jpg), CC0",
      "creator": "Terry Kearney from liverpool, merseyside",
      "height": 3264,
      "id": "File:Playtime at sunset. ( Explored ) - Flickr - Oneterry AKA Terry Kearney.jpg (pageid 176630081)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Playtime_at_sunset._(_Explored_)_-_Flickr_-_Oneterry_AKA_Terry_Kearney.jpg",
      "sha1": "aad4f624bb71a1f20066848be34e4f0b8048c013",
      "slot": "S17",
      "source": "wikimedia-commons",
      "title": "Playtime at sunset. ( Explored ) - Flickr - Oneterry AKA Terry Kearney",
      "url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Playtime_at_sunset._%28_Explored_%29_-_Flickr_-_Oneterry_AKA_Terry_Kearney.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 4352
    },
    {
      "as_of": "2026-10-08",
      "attribution": "Tim Tams and Nuts on a Birthday Cake With Candles during her Anniversary by Brassluff (https://commons.wikimedia.org/wiki/File:Tim_Tams_and_Nuts_on_a_Birthday_Cake_With_Candles_during_her_Anniversary.jpg), CC0",
      "creator": "Brassluff",
      "height": 4032,
      "id": "File:Tim Tams and Nuts on a Birthday Cake With Candles during her Anniversary.jpg (pageid 191012522)",
      "license": "CC0",
      "license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "page_url": "https://commons.wikimedia.org/wiki/File:Tim_Tams_and_Nuts_on_a_Birthday_Cake_With_Candles_during_her_Anniversary.jpg",
      "sha1": "01bb98ed2da1c86d8ff35548c2006369c952da18",
      "slot": "S20",
      "source": "wikimedia-commons",
      "title": "Tim Tams and Nuts on a Birthday Cake With Candles during her Anniversary",
      "url": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Tim_Tams_and_Nuts_on_a_Birthday_Cake_With_Candles_during_her_Anniversary.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original",
      "width": 3024
    }
  ]
}
```
<!-- fallback-selection:end -->
