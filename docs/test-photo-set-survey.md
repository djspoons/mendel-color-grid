# Test photo set survey (license-filtered API route)

**Partial result**: 11 of 20 photos selected; see Coverage mix for the cells left unfilled.
Run notes (requests that failed or candidates rejected; the run carried on): 50. First entries:
  - request failed: https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&list=search&srnamespace=6&srlimit=1&srinfo=totalhits&srsearch=filetype%3Abitmap+incategory%3ACC-Zero+kitchen (HTTP 429)
  - c01: skipped openverse b9ce1263-d73c-49bd-bd19-e7d3c2b9d36e: real size 960x640 below minimum
  - c01: skipped openverse bbdc9b19-43a9-4d96-9239-3ae8c6e8bb4e: real size 960x640 below minimum
  - c01: skipped openverse 758d7eb2-df2b-4d8f-b858-44225dce7ba5: real size 960x640 below minimum
  - c01: skipped openverse b6cf750c-b4d8-4f54-a278-d03dbf81be34: not a readable JPEG
  - request failed: https://api.openverse.org/v1/images/?q=child+playing+outdoors&license=cc0%2Cpdm&category=photograph&mature=false&page_size=20&page=1&extension=jpg (HTTP 403)
  - c03: skipped openverse c125a9cf-2d76-4e80-b419-b3e54c9c0649: real size 960x640 below minimum
  - c03: skipped openverse eaeb9bd8-fe2e-4b99-8f22-481ccc110c21: real size 960x1440 below minimum
  - c04: skipped openverse f8d0fc12-0b2b-4add-869a-e2fbe4d4db7a: real size 960x1440 below minimum
  - c05: skipped openverse b88fcaca-736b-4bd4-96d1-931f32f86d5d: real size 960x640 below minimum
  - c05: skipped openverse 05f52d78-5ccb-4db7-b118-083e848c5f4b: real size 960x640 below minimum
  - c06: skipped openverse f2adef73-e513-427a-8b55-77675311c516: real size 960x1440 below minimum
  - c08: skipped openverse 194f4506-0485-47b8-a8c2-3759ee2c06d0: real size 960x640 below minimum
  - c08: skipped openverse 7673b1b2-0607-45f3-84cb-cd5ac766789a: real size 960x640 below minimum
  - c08: skipped openverse cd4c4860-4d0a-4085-81ce-c74159fe9638: real size 960x1440 below minimum

## What was read

As-of date (UTC): **2026-10-08**

Sources visited: Openverse API (https://api.openverse.org/v1), Wikimedia Commons API (https://commons.wikimedia.org/w/api.php).
Other sources in the next section were not queried (they need keys or have unclear terms).

Candidate counts per source and route (CC0 / public-domain filter applied in each query):

| Source | Route | Query / category | Filter | Count |
|---|---|---|---|---|
| Openverse | search API | child | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | child | namespace File, bitmap | 32,889 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | child | namespace File, bitmap | 3,716 |
| Openverse | search API | children playing | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | children playing | namespace File, bitmap | 2,016 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | children playing | namespace File, bitmap | 299 |
| Openverse | search API | family | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | family | namespace File, bitmap | 298,819 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | family | namespace File, bitmap | 11,221 |
| Openverse | search API | dog | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | dog | namespace File, bitmap | 13,660 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | dog | namespace File, bitmap | 1,602 |
| Openverse | search API | cat | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | cat | namespace File, bitmap | 1,041,159 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | cat | namespace File, bitmap | 12,727 |
| Openverse | search API | kitchen | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | kitchen | namespace File, bitmap | NOT READ (request failed) |
| Wikimedia Commons | search (list=search, incategory:PD-self) | kitchen | namespace File, bitmap | 115,219 |
| Openverse | search API | birthday | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | birthday | namespace File, bitmap | 5,063 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | birthday | namespace File, bitmap | 640 |
| Openverse | search API | picnic | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | search (list=search, incategory:CC-Zero) | picnic | namespace File, bitmap | 1,570 |
| Wikimedia Commons | search (list=search, incategory:PD-self) | picnic | namespace File, bitmap | 850 |
| Openverse | search API, source=stocksnap | family | license=cc0,pdm; category=photograph | 240 |
| Openverse | search API, source=wikimedia | family | license=cc0,pdm; category=photograph | 0 (zero: failed read, not a finding) |
| Openverse | search API, source=flickr | family | license=cc0,pdm; category=photograph | 240 |
| Wikimedia Commons | category listing (categoryinfo) | Category:PD-self | all file types, all subjects | 1,617,539 |
| Wikimedia Commons | category listing (categoryinfo) | Category:CC-Zero | all file types, all subjects | 9,875,368 |

Openverse stats route (`/v1/images/stats/`, all licenses, before any filter): 52 sources, 915,519,784 images in total. Largest: flickr 536,219,600, inaturalist 266,268,617, wikimedia 88,962,441, europeana 13,841,364, smithsonian_national_museum_of_natural_history 4,990,743, rawpixel 1,268,095, geographorguk 1,090,119, met 498,428.

Where routes disagree: for "family", Openverse reports 0 CC0/PDM Wikimedia-sourced photographs, while Commons' own search reports 298,819 + 11,221 files across incategory:CC-Zero and incategory:PD-self. They count different things (Openverse's license filter and 'photograph' category versus Commons categories and bitmap files), so neither is a subset of the other; Commons' own search was used for Commons candidates.

Candidate pools per grid cell (raw API hits, then after resolution / keyword / duplicate filters):

| Cell | Search terms | Openverse hits | Commons hits | Usable |
|---|---|---|---|---|
| c01 | child portrait smiling | 40 | 2 | 38 |
| c02 | child playing outdoors | 0 | 6 | 6 |
| c03 | child playing in park | 40 | 23 | 61 |
| c04 | child portrait indoors | 3 | 0 | 1 |
| c05 | child playing at home | 40 | 26 | 61 |
| c06 | child evening dusk | 1 | 0 | 1 |
| c07 | child silhouette sunset | 2 | 2 | 4 |
| c08 | children playing together | 40 | 55 | 27 |
| c09 | family picnic park | 37 | 51 | 12 |
| c10 | family dinner table | 13 | 1 | 1 |
| c11 | birthday party candles | 11 | 4 | 11 |
| c12 | mother with child outdoors | 0 | 2 | 1 |
| c13 | father holding baby | 16 | 7 | 11 |
| c14 | family sunset beach | 21 | 5 | 2 |
| c15 | dog portrait | 40 | 72 | 60 |
| c16 | dog running in park | 7 | 0 | 5 |
| c17 | cat on sofa at home | 5 | 2 | 1 |
| c18 | cat at night | 40 | 83 | 35 |
| c19 | toys on floor children room | 1 | 1 | 2 |
| c20 | backyard garden house | 10 | 43 | 39 |

## Candidate sources

| Source | License | Commit and reuse clearly allowed? | Attribution | Scriptable fetch? | Rights flag |
|---|---|---|---|---|---|
| Openverse (api.openverse.org) | Aggregator; per-item license field (CC0 1.0, PDM 1.0 kept here) | Yes for CC0/PDM; the upstream site's own terms are still on the landing page | None required for CC0/PDM | Yes, anonymous JSON API, rate limited | Check upstream landing page per photo |
| Wikimedia Commons | Per-file license templates (CC0, PD-self, other PD) | Yes for CC0 and PD-self; other PD tags vary by country | None for CC0/PD; keep the file page link | Yes, MediaWiki API with a User-Agent header, SHA-1 in the API | Personality / model rights are not covered by the copyright license |
| StockSnap (via Openverse source filter) | CC0 1.0 as listed by Openverse | Yes | None | Through Openverse only; not queried directly | Model releases not stated |
| Unsplash | Unsplash License (not CC0) | Unclear: free use, but no compiling into a competing library | Not required | Official API needs a key; not queried | RIGHTS UNCLEAR for committing to a repository |
| Pexels | Pexels License (not CC0) | Unclear for redistribution of unmodified files | Not required | API needs a key; not queried | RIGHTS UNCLEAR |
| Pixabay | Pixabay Content License (not CC0) | Unclear for redistribution as-is; identifiable people carry extra limits | Not required | API needs a key; not queried | RIGHTS UNCLEAR |
| Team-shot photos | Owned by the team | Yes, with written releases from every person shown | None | Not scriptable (manual upload) | Needs releases, especially for children |

Rows other than Openverse and Wikimedia Commons describe the sources' published terms as understood when this script was written; this run did not read or verify them.

## Recommended set

11 of 20 target photos selected. Selection is pinned in `docs/test-photo-set-manifest.json` (ID, URL, license, SHA-256, as-of date 2026-10-08); a rerun of the fetch script retrieves exactly these.
| # | ID / URL | Creator | License | Attribution | Subject | Lighting | Framing | Resolution |
|---|---|---|---|---|---|---|---|---|
| 1 | commons:29223843 (https://commons.wikimedia.org/wiki/File:Annie_and_John_Glenn_1965_in_Schiphol.jpg) | Jack de Nijs for Anefo | CC0 (api: cc0 1.0) | "Annie and John Glenn 1965 in Schiphol.jpg" by Jack de Nijs for Anefo, CC0, https://commons.wikimedia.org/wiki/File:Annie_and_John_Glenn_1965_in_Schiphol.jpg | single child | bright | close-up | 2076x1468 |
| 2 | commons:11141101 (https://commons.wikimedia.org/wiki/File:Child_playing_in_the_sand_at_Misquamicut_Beach.JPG) | Juliancolton | Public domain (api: pd ) | "Child playing in the sand at Misquamicut Beach.JPG" by Juliancolton, Public domain, https://commons.wikimedia.org/wiki/File:Child_playing_in_the_sand_at_Misquamicut_Beach.JPG | single child | bright | medium | 3872x2592 |
| 3 | commons:56878775 (https://commons.wikimedia.org/wiki/File:Golders_to_Gladstone_(13)_(32426272474).jpg) | Camden Cyclists | CC0 (api: cc0 1.0) | "Golders to Gladstone (13) (32426272474).jpg" by Camden Cyclists, CC0, https://commons.wikimedia.org/wiki/File:Golders_to_Gladstone_(13)_(32426272474).jpg | single child | bright | wide | 2048x1630 |
| 4 | commons:107332386 (https://commons.wikimedia.org/wiki/File:The_Chicago_Sunday_Bee_About_Books_13_Oct._1946.jpg) | The Chicago Bee, Edited by E. R. CAMPFIELD | CC0 (api: cc0 1.0) | "The Chicago Sunday Bee About Books 13 Oct. 1946.jpg" by The Chicago Bee, Edited by E. R. CAMPFIELD, CC0, https://commons.wikimedia.org/wiki/File:The_Chicago_Sunday_Bee_About_Books_13_Oct._1946.jpg | single child | indoor | medium | 4681x6812 |
| 5 | commons:61635915 (https://commons.wikimedia.org/wiki/File:Child_entering_the_ocean_(Unsplash).jpg) | Viktor Jakovlev apviktor | CC0 (api: cc0 1.0) | "Child entering the ocean (Unsplash).jpg" by Viktor Jakovlev apviktor, CC0, https://commons.wikimedia.org/wiki/File:Child_entering_the_ocean_(Unsplash).jpg | single child | backlit | medium | 5831x3893 |
| 6 | commons:143384222 (https://commons.wikimedia.org/wiki/File:Christmas_address_by_President_of_Ukraine_Volodymyr_Zelenskyy._-_53420009916.jpg) | President Of Ukraine | CC0 (api: cc0 1.0) | "Christmas address by President of Ukraine Volodymyr Zelenskyy. - 53420009916.jpg" by President Of Ukraine, CC0, https://commons.wikimedia.org/wiki/File:Christmas_address_by_President_of_Ukraine_Volodymyr_Zelenskyy._-_53420009916.jpg | group | indoor | medium | 3000x2001 |
| 7 | commons:45011003 (https://commons.wikimedia.org/wiki/File:2015%EB%85%84_10%EC%9B%94_%EA%B2%BD%EA%B8%B0%EB%8F%84_%EA%B3%BC%EC%B2%9C%EC%8B%9C_%EC%A3%BC%EA%B3%B55%EB%8B%A8%EC%A7%80_%EC%95%84%ED%8C%8C%ED%8A%B8_20151024_DSC04531_%EC%B5%9C%EA%B4%91%EB%AA%A8_Sony_RX10.JPG) | 최광모 (Choe Kwangmo) | CC0 (api: cc0 1.0) | "2015년 10월 경기도 과천시 주공5단지 아파트 20151024 DSC04531 최광모 Sony RX10.JPG" by 최광모 (Choe Kwangmo), CC0, https://commons.wikimedia.org/wiki/File:2015%EB%85%84_10%EC%9B%94_%EA%B2%BD%EA%B8%B0%EB%8F%84_%EA%B3%BC%EC%B2%9C%EC%8B%9C_%EC%A3%BC%EA%B3%B55%EB%8B%A8%EC%A7%80_%EC%95%84%ED%8C%8C%ED%8A%B8_20151024_DSC04531_%EC%B5%9C%EA%B4%91%EB%AA%A8_Sony_RX10.JPG | group | low light | wide | 5472x3648 |
| 8 | commons:53202921 (https://commons.wikimedia.org/wiki/File:Anyas%C3%A1g,_Baja.jpg) | Csanády | CC0 (api: cc0 1.0) | "Anyaság, Baja.jpg" by Csanády, CC0, https://commons.wikimedia.org/wiki/File:Anyas%C3%A1g,_Baja.jpg | adults with children | bright | medium | 2592x1944 |
| 9 | commons:61705751 (https://commons.wikimedia.org/wiki/File:Family_watching_beach_sunset_(Unsplash).jpg) | David Straight davidstraight | CC0 (api: cc0 1.0) | "Family watching beach sunset (Unsplash).jpg" by David Straight davidstraight, CC0, https://commons.wikimedia.org/wiki/File:Family_watching_beach_sunset_(Unsplash).jpg | adults with children | backlit | wide | 4608x3072 |
| 10 | commons:120692481 (https://commons.wikimedia.org/wiki/File:A_female_boxer_dog_in_Iran_%D9%80_Mostafa_Meraji_Canon_Photography_08.jpg) | Mostafameraji | CC0 (api: cc0 1.0) | "A female boxer dog in Iran ـ Mostafa Meraji Canon Photography 08.jpg" by Mostafameraji, CC0, https://commons.wikimedia.org/wiki/File:A_female_boxer_dog_in_Iran_%D9%80_Mostafa_Meraji_Canon_Photography_08.jpg | pets | bright | close-up | 3333x5000 |
| 11 | commons:65100266 (https://commons.wikimedia.org/wiki/File:%22Assad_Ibn_Kariba_Launches_a_Night_Attack_on_the_Camp_of_Malik_Iraj%22,_Folio_from_a_Hamzanama_(The_Adventures_of_Hamza)_MET_CAT_10_DETAILr1_89A.jpg) | Attributed to Basawan / Attributed to Tara | CC0 (api: cc0 1.0) | ""Assad Ibn Kariba Launches a Night Attack on the Camp of Malik Iraj", Folio from a Hamzanama (The Adventures of Hamza) MET CAT 10 DETAILr1 89A.jpg" by Attributed to Basawan / Attributed to Tara, CC0, https://commons.wikimedia.org/wiki/File:%22Assad_Ibn_Kariba_Launches_a_Night_Attack_on_the_Camp_of_Malik_Iraj%22,_Folio_from_a_Hamzanama_(The_Adventures_of_Hamza)_MET_CAT_10_DETAILr1_89A.jpg | pets | low light | close-up | 1163x2000 |

## Coverage mix

Labels come from the grid cell a photo filled: the search terms plus a keyword check on the title, tags, description and categories. **No photo was inspected visually**, so subject, lighting and framing are unverified metadata-based labels.

Subject: single child 5, group 2, adults with children 2, pets 2, objects 0

Lighting: bright 5, indoor 2, low light 2, backlit 2

Framing: close-up 3, medium 5, wide 3

Gaps (subject x lighting combinations with no photo):

| Subject | Lighting | Reason |
|---|---|---|
| single child | low light | grid cell c06 found no usable candidate (1 after filters) |
| group | bright | grid cell c08 found no usable candidate (27 after filters) |
| group | backlit | not in the 20-cell grid; 20 photos cannot cover all 60 combinations |
| adults with children | indoor | grid cell c13 found no usable candidate (11 after filters) |
| adults with children | low light | not in the 20-cell grid; 20 photos cannot cover all 60 combinations |
| pets | indoor | grid cell c17 found no usable candidate (1 after filters) |
| pets | backlit | not in the 20-cell grid; 20 photos cannot cover all 60 combinations |
| objects | bright | grid cell c20 found no usable candidate (39 after filters) |
| objects | indoor | grid cell c19 found no usable candidate (2 after filters) |
| objects | low light | not in the 20-cell grid; 20 photos cannot cover all 60 combinations |
| objects | backlit | not in the 20-cell grid; 20 photos cannot cover all 60 combinations |

Unfilled cells: c04, c06, c08, c09, c13, c16, c17, c19, c20

## Rights risks

- A CC0 or public-domain tag covers copyright only. It does not give a model release for identifiable people, and none of the APIs state whether a release exists. Children are the sensitive case: a parent or the uploader may have posted the photo without a signed release.
- Photos here whose subject is a child, a group or adults with children should be treated as unreleased until a person has checked the source page. Prefer silhouettes, backs of heads and distant shots; avoid close-up faces of children where no release is stated.
- Public-domain flags on Commons other than CC0 and PD-self depend on country and date; this script only accepts CC0, 'Public domain' and PD-* short names, and a human should confirm the individual file page.
- Avoid photos with visible brand logos, artwork, house numbers or licence plates (property concerns), and avoid anything from Unsplash, Pexels or Pixabay in the repository until their redistribution terms are reviewed.
- Aggregators such as Openverse can lag behind upstream license changes; the landing URL recorded for each photo is the place to recheck.

## Fetch script

- Script: `docs/fetch_test_photos.py` (standard library only); input `docs/test-photo-set-manifest.json`.
- Run: `python docs/fetch_test_photos.py [--dest test-photos] [--manifest PATH]`.
- Downloads each photo by its source ID/URL, verifies the SHA-256 recorded in the manifest, and writes `ATTRIBUTION.txt` beside the photos.
- Rerunning keeps files that already match their checksum; downloads retry on network errors, 429 and 5xx; a changed URL falls back to Commons `Special:FilePath` or the Openverse detail endpoint; mismatching or missing photos make the exit status non-zero and are listed.
- The manifest is regenerated by `python scripts/survey_test_photos.py`, which also rewrites this document. Because the live APIs change, regenerating can pick different photos; commit the manifest to keep the set fixed.
- Limitation: the checksums were taken at survey time from the URL the APIs gave; they were not cross-checked against a second independent copy except for Commons' own SHA-1.

## Open questions

- Round 2 (visual review): does a person agree with each photo's subject, lighting and framing label, and with the child-related rights judgement?
- Round 3 (rights): is a CC0 tag with no model release acceptable for photos of identifiable children, or should those cells use silhouettes or team-shot photos?
- Round 4 (sources): should Unsplash, Pexels or Pixabay be reviewed with API keys, or are CC0/PD sources enough?
- Round 5 (storage): commit the 20 JPEGs to the repository, or keep only the manifest and fetch on demand?
