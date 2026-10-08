# Picture method results: average-then-snap

Generated 2026-10-08 20:01 UTC by `python run_picture_method.py`.
Method: average each cell's pixels, then snap that average to the nearest of the 24 Crayola crayons in CIE Lab.

## Run notes

- Every image was read and no fallback was taken.
- Contrast/saturation boost: on (contrast x1.10, saturation x1.15).

## What was read

- Images read: 11 of 11 expected.
- Densities (columns x rows): 24x32, 36x48, 48x64.
- Palette: the classic Crayola 24-count box; hex values below are the ones this run used. Cell numbers are the 1-24 positions in this list.

| image | file | source | license | pixels (as saved) | SHA-256 of saved file | 3:4 crop | notes |
|---|---|---|---|---|---|---|---|
| 01-astronaut | photos/01-astronaut.jpg | skimage.data.astronaut() | public domain (NASA photo), as documented by scikit-image | 512x512 | `011901a3f9084e22497e2b27642b44a39e8965c4c2febc5ddf2c3ccf298c8787` | crop removes the sides | bundled array re-encoded as JPEG quality 95 |
| 02-chelsea-cat | photos/02-chelsea-cat.jpg | skimage.data.chelsea() | CC0, as documented by scikit-image | 451x300 | `e8605ae62ddd946bef56bba73435937edcab675f8ef20cdcee29fdbf2d94045f` | crop removes the sides | bundled array re-encoded as JPEG quality 95 |
| 03-coffee | photos/03-coffee.jpg | skimage.data.coffee() | CC0, as documented by scikit-image | 600x400 | `80e2b46bbd310f215a6381ceac2ef7a403c23874ec48b3637cd74177e31ed4ea` | crop removes the sides | bundled array re-encoded as JPEG quality 95 |
| 04-rocket | photos/04-rocket.jpg | skimage.data.rocket() | public domain, as documented by scikit-image | 640x427 | `2d3d62a61bf417fd93253df812c357b86fdfcd50d74b4280ae252455fe7064db` | crop removes the sides | bundled array re-encoded as JPEG quality 95 |
| 05-raccoon | photos/05-raccoon.jpg | scipy.datasets.face() | public domain (public-domain-image.com), as documented by SciPy | 1024x768 | `1324d7414eec1ec09bbe1998f78a4c1854fd6baec9a1e09286232cab5dd26a17` | crop removes the sides | bundled array re-encoded as JPEG quality 95 |
| 06-mona-lisa | photos/06-mona-lisa.jpg | https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg | Public domain | 1920x2861 | `276868845c54914913c965b208eec75db55c1675489e563852f155c5db58b536` | crop removes the top and bottom | original on Commons: 7479x11146 px; fetched the 1600px-wide thumbnail |
| 07-migrant-mother | photos/07-migrant-mother.jpg | https://commons.wikimedia.org/wiki/File:Lange-MigrantMother02.jpg | Public domain | 1920x2496 | `e6657df96f6dadede759d88c6c3ebc14dc956633c246a3a1046a47ebf5c17afd` | crop removes the sides | original on Commons: 6205x8066 px; fetched the 1600px-wide thumbnail |
| 08-lunch-atop-skyscraper | photos/08-lunch-atop-skyscraper.jpg | https://commons.wikimedia.org/wiki/File:Lunch_atop_a_Skyscraper.jpg | Public domain | 1920x1482 | `3a487894b9c1462dbe0813ffb1c82d8e0508b440337cee1a3ef34a683e559b1f` | crop removes the sides | original on Commons: 8192x6322 px; fetched the 1600px-wide thumbnail |
| 09-golden-retriever | photos/09-golden-retriever.jpg | https://commons.wikimedia.org/wiki/File:Golden_Retriever_Dukedestiny01.jpg | Public domain | 1024x768 | `7a7d156fcb6fe815670924619cf4bb2e310232a93e6b7fea64505d1dac486ec5` | crop removes the sides | original on Commons: 1024x768 px; fetched the original |
| 10-hopetoun-falls | photos/10-hopetoun-falls.jpg | https://commons.wikimedia.org/wiki/File:Hopetoun_falls.jpg | CC BY-SA 3.0 | 1920x1280 | `afc9ddf298d06298520e981f5b7fb7d9c89a6de68e8bd8363091c59405cc7fcd` | crop removes the sides | original on Commons: 3072x2048 px; fetched the 1600px-wide thumbnail |
| 11-shibuya-crossing | photos/11-shibuya-crossing.jpg | https://commons.wikimedia.org/wiki/File:Tokyo_Shibuya_Scramble_Crossing_2018-10-09.jpg | CC BY-SA 2.0 | 1920x1280 | `615151cfc947a72008a1d8aa12ba606d437bcc5d656ff87305228e094f916edd` | crop removes the sides | original on Commons: 5853x3902 px; fetched the 1600px-wide thumbnail |

Palette (number, name, hex):

| # | crayon | hex |
|---|---|---|
| 1 | Red | `#EE204D` |
| 2 | Yellow | `#FCE883` |
| 3 | Blue | `#1F75FE` |
| 4 | Brown | `#B4674D` |
| 5 | Orange | `#FF7538` |
| 6 | Green | `#1CAC78` |
| 7 | Violet | `#926EAE` |
| 8 | Black | `#000000` |
| 9 | Carnation Pink | `#FFAACC` |
| 10 | Yellow Green | `#C5E384` |
| 11 | Blue Green | `#0D98BA` |
| 12 | Red Orange | `#FF5349` |
| 13 | Red Violet | `#C0448F` |
| 14 | Yellow Orange | `#FFB653` |
| 15 | Blue Violet | `#7366BD` |
| 16 | White | `#FFFFFF` |
| 17 | Violet Red | `#F75394` |
| 18 | Dandelion | `#FDDB6D` |
| 19 | Cerulean | `#1DACD6` |
| 20 | Apricot | `#FDD9B5` |
| 21 | Scarlet | `#FC2847` |
| 22 | Green Yellow | `#F0E891` |
| 23 | Indigo | `#5D76CB` |
| 24 | Gray | `#95918C` |

## Method: average then snap

1. Center-crop the source to 3:4 portrait (width:height).
2. Contrast/saturation boost before averaging: **on (contrast x1.10, saturation x1.15)**. The original shown beside each preview is the unboosted crop.
3. Split the cropped picture into the fixed grid and take each cell's mean sRGB color (plain average of every pixel in the cell).
4. Snap each mean to the nearest of the 24 crayons by Euclidean distance in CIE Lab (D65), not RGB.

Code: `picture_method/average_then_snap.py` (steps 2-4), `picture_method/preprocess.py` (steps 1 and 3 grid split), `picture_method/palette.py` (crayons, Lab). Previews, blank grids and metrics are shared code (`render.py`, `metrics.py`) that any method can reuse.

Colored preview files are flat cells with no lines. Blank grids are grayscale with uniform thin lines and the crayon number (1-24) in each cell. Files are under `docs/picture-method/average-then-snap/`.

## Previews

### Contact sheets (all 11 images, pinned order; original left, preview right)

**24x32**

![contact sheet 24x32](picture-method/average-then-snap/contact-24x32.png)

**36x48**

![contact sheet 36x48](picture-method/average-then-snap/contact-36x48.png)

**48x64**

![contact sheet 48x64](picture-method/average-then-snap/contact-48x64.png)

### Per image and density (original beside colored preview, then blank numbered grid)

#### 01-astronaut

24x32: [blank grid](picture-method/average-then-snap/01-astronaut_24x32_blank.png)

![01-astronaut 24x32](picture-method/average-then-snap/01-astronaut_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/01-astronaut_36x48_blank.png)

![01-astronaut 36x48](picture-method/average-then-snap/01-astronaut_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/01-astronaut_48x64_blank.png)

![01-astronaut 48x64](picture-method/average-then-snap/01-astronaut_48x64_compare.png)


#### 02-chelsea-cat

24x32: [blank grid](picture-method/average-then-snap/02-chelsea-cat_24x32_blank.png)

![02-chelsea-cat 24x32](picture-method/average-then-snap/02-chelsea-cat_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/02-chelsea-cat_36x48_blank.png)

![02-chelsea-cat 36x48](picture-method/average-then-snap/02-chelsea-cat_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/02-chelsea-cat_48x64_blank.png)

![02-chelsea-cat 48x64](picture-method/average-then-snap/02-chelsea-cat_48x64_compare.png)


#### 03-coffee

24x32: [blank grid](picture-method/average-then-snap/03-coffee_24x32_blank.png)

![03-coffee 24x32](picture-method/average-then-snap/03-coffee_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/03-coffee_36x48_blank.png)

![03-coffee 36x48](picture-method/average-then-snap/03-coffee_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/03-coffee_48x64_blank.png)

![03-coffee 48x64](picture-method/average-then-snap/03-coffee_48x64_compare.png)


#### 04-rocket

24x32: [blank grid](picture-method/average-then-snap/04-rocket_24x32_blank.png)

![04-rocket 24x32](picture-method/average-then-snap/04-rocket_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/04-rocket_36x48_blank.png)

![04-rocket 36x48](picture-method/average-then-snap/04-rocket_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/04-rocket_48x64_blank.png)

![04-rocket 48x64](picture-method/average-then-snap/04-rocket_48x64_compare.png)


#### 05-raccoon

24x32: [blank grid](picture-method/average-then-snap/05-raccoon_24x32_blank.png)

![05-raccoon 24x32](picture-method/average-then-snap/05-raccoon_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/05-raccoon_36x48_blank.png)

![05-raccoon 36x48](picture-method/average-then-snap/05-raccoon_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/05-raccoon_48x64_blank.png)

![05-raccoon 48x64](picture-method/average-then-snap/05-raccoon_48x64_compare.png)


#### 06-mona-lisa

24x32: [blank grid](picture-method/average-then-snap/06-mona-lisa_24x32_blank.png)

![06-mona-lisa 24x32](picture-method/average-then-snap/06-mona-lisa_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/06-mona-lisa_36x48_blank.png)

![06-mona-lisa 36x48](picture-method/average-then-snap/06-mona-lisa_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/06-mona-lisa_48x64_blank.png)

![06-mona-lisa 48x64](picture-method/average-then-snap/06-mona-lisa_48x64_compare.png)


#### 07-migrant-mother

24x32: [blank grid](picture-method/average-then-snap/07-migrant-mother_24x32_blank.png)

![07-migrant-mother 24x32](picture-method/average-then-snap/07-migrant-mother_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/07-migrant-mother_36x48_blank.png)

![07-migrant-mother 36x48](picture-method/average-then-snap/07-migrant-mother_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/07-migrant-mother_48x64_blank.png)

![07-migrant-mother 48x64](picture-method/average-then-snap/07-migrant-mother_48x64_compare.png)


#### 08-lunch-atop-skyscraper

24x32: [blank grid](picture-method/average-then-snap/08-lunch-atop-skyscraper_24x32_blank.png)

![08-lunch-atop-skyscraper 24x32](picture-method/average-then-snap/08-lunch-atop-skyscraper_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/08-lunch-atop-skyscraper_36x48_blank.png)

![08-lunch-atop-skyscraper 36x48](picture-method/average-then-snap/08-lunch-atop-skyscraper_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/08-lunch-atop-skyscraper_48x64_blank.png)

![08-lunch-atop-skyscraper 48x64](picture-method/average-then-snap/08-lunch-atop-skyscraper_48x64_compare.png)


#### 09-golden-retriever

24x32: [blank grid](picture-method/average-then-snap/09-golden-retriever_24x32_blank.png)

![09-golden-retriever 24x32](picture-method/average-then-snap/09-golden-retriever_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/09-golden-retriever_36x48_blank.png)

![09-golden-retriever 36x48](picture-method/average-then-snap/09-golden-retriever_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/09-golden-retriever_48x64_blank.png)

![09-golden-retriever 48x64](picture-method/average-then-snap/09-golden-retriever_48x64_compare.png)


#### 10-hopetoun-falls

24x32: [blank grid](picture-method/average-then-snap/10-hopetoun-falls_24x32_blank.png)

![10-hopetoun-falls 24x32](picture-method/average-then-snap/10-hopetoun-falls_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/10-hopetoun-falls_36x48_blank.png)

![10-hopetoun-falls 36x48](picture-method/average-then-snap/10-hopetoun-falls_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/10-hopetoun-falls_48x64_blank.png)

![10-hopetoun-falls 48x64](picture-method/average-then-snap/10-hopetoun-falls_48x64_compare.png)


#### 11-shibuya-crossing

24x32: [blank grid](picture-method/average-then-snap/11-shibuya-crossing_24x32_blank.png)

![11-shibuya-crossing 24x32](picture-method/average-then-snap/11-shibuya-crossing_24x32_compare.png)

36x48: [blank grid](picture-method/average-then-snap/11-shibuya-crossing_36x48_blank.png)

![11-shibuya-crossing 36x48](picture-method/average-then-snap/11-shibuya-crossing_36x48_compare.png)

48x64: [blank grid](picture-method/average-then-snap/11-shibuya-crossing_48x64_blank.png)

![11-shibuya-crossing 48x64](picture-method/average-then-snap/11-shibuya-crossing_48x64_compare.png)


## Recognizability notes

**Automated proxy, not human viewing.** No person or vision model looked at these previews. A preview counts as recognizable (proxy) when the light/dark pattern survives (correlation of Lab lightness between the original's cell means and the snapped crayons >= 0.85), at least 5 crayons are used, and the mean Lab distance to the original cell colors is <= 30. The thresholds are judgment calls. A pass means the picture's large shapes were kept, not that a child would name the subject; look at the contact sheets for that.

| image | density | L correlation | mean dE | crayons | note |
|---|---|---|---|---|---|
| 01-astronaut | 24x32 | 0.922 | 16.2 | 11 | recognizable (proxy) |
| 01-astronaut | 36x48 | 0.922 | 16.2 | 13 | recognizable (proxy) |
| 01-astronaut | 48x64 | 0.928 | 16.0 | 12 | recognizable (proxy) |
| 02-chelsea-cat | 24x32 | 0.599 | 19.7 | 5 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.60 < 0.85) |
| 02-chelsea-cat | 36x48 | 0.632 | 19.7 | 5 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.63 < 0.85) |
| 02-chelsea-cat | 48x64 | 0.651 | 19.8 | 6 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.65 < 0.85) |
| 03-coffee | 24x32 | 0.898 | 22.3 | 8 | recognizable (proxy) |
| 03-coffee | 36x48 | 0.900 | 22.1 | 8 | recognizable (proxy) |
| 03-coffee | 48x64 | 0.905 | 21.9 | 8 | recognizable (proxy) |
| 04-rocket | 24x32 | 0.748 | 29.2 | 10 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.75 < 0.85) |
| 04-rocket | 36x48 | 0.751 | 29.1 | 10 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.75 < 0.85) |
| 04-rocket | 48x64 | 0.744 | 29.1 | 12 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.74 < 0.85) |
| 05-raccoon | 24x32 | 0.854 | 19.6 | 6 | recognizable (proxy) |
| 05-raccoon | 36x48 | 0.862 | 19.5 | 6 | recognizable (proxy) |
| 05-raccoon | 48x64 | 0.864 | 19.7 | 6 | recognizable (proxy) |
| 06-mona-lisa | 24x32 | 0.917 | 23.4 | 8 | recognizable (proxy) |
| 06-mona-lisa | 36x48 | 0.919 | 23.3 | 8 | recognizable (proxy) |
| 06-mona-lisa | 48x64 | 0.921 | 23.2 | 8 | recognizable (proxy) |
| 07-migrant-mother | 24x32 | 0.832 | 15.1 | 3 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.83 < 0.85); only 3 crayons used |
| 07-migrant-mother | 36x48 | 0.841 | 14.9 | 3 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.84 < 0.85); only 3 crayons used |
| 07-migrant-mother | 48x64 | 0.847 | 14.9 | 3 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.85 < 0.85); only 3 crayons used |
| 08-lunch-atop-skyscraper | 24x32 | 0.815 | 18.1 | 3 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.82 < 0.85); only 3 crayons used |
| 08-lunch-atop-skyscraper | 36x48 | 0.831 | 17.9 | 3 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.83 < 0.85); only 3 crayons used |
| 08-lunch-atop-skyscraper | 48x64 | 0.844 | 17.8 | 3 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.84 < 0.85); only 3 crayons used |
| 09-golden-retriever | 24x32 | 0.823 | 21.0 | 7 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.82 < 0.85) |
| 09-golden-retriever | 36x48 | 0.822 | 21.0 | 8 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.82 < 0.85) |
| 09-golden-retriever | 48x64 | 0.823 | 21.0 | 8 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.82 < 0.85) |
| 10-hopetoun-falls | 24x32 | 0.834 | 19.6 | 7 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.83 < 0.85) |
| 10-hopetoun-falls | 36x48 | 0.840 | 19.7 | 8 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.84 < 0.85) |
| 10-hopetoun-falls | 48x64 | 0.846 | 19.6 | 9 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.85 < 0.85) |
| 11-shibuya-crossing | 24x32 | 0.684 | 19.0 | 18 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.68 < 0.85) |
| 11-shibuya-crossing | 36x48 | 0.704 | 19.6 | 19 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.70 < 0.85) |
| 11-shibuya-crossing | 48x64 | 0.721 | 19.6 | 20 | NOT recognizable (proxy): light/dark structure lost (L correlation 0.72 < 0.85) |

### Roll-up by category

| category | density | images | recognizable (proxy) | mean L correlation | mean dE |
|---|---|---|---|---|---|
| portrait | 24x32 | 01-astronaut, 06-mona-lisa | 2/2 | 0.919 | 19.8 |
| portrait | 36x48 | 01-astronaut, 06-mona-lisa | 2/2 | 0.920 | 19.7 |
| portrait | 48x64 | 01-astronaut, 06-mona-lisa | 2/2 | 0.925 | 19.6 |
| group | 24x32 | 07-migrant-mother, 08-lunch-atop-skyscraper | 0/2 | 0.823 | 16.6 |
| group | 36x48 | 07-migrant-mother, 08-lunch-atop-skyscraper | 0/2 | 0.836 | 16.4 |
| group | 48x64 | 07-migrant-mother, 08-lunch-atop-skyscraper | 0/2 | 0.845 | 16.4 |
| pet or animal | 24x32 | 02-chelsea-cat, 05-raccoon, 09-golden-retriever | 1/3 | 0.759 | 20.1 |
| pet or animal | 36x48 | 02-chelsea-cat, 05-raccoon, 09-golden-retriever | 1/3 | 0.772 | 20.1 |
| pet or animal | 48x64 | 02-chelsea-cat, 05-raccoon, 09-golden-retriever | 1/3 | 0.779 | 20.2 |
| outdoor | 24x32 | 04-rocket, 10-hopetoun-falls | 0/2 | 0.791 | 24.4 |
| outdoor | 36x48 | 04-rocket, 10-hopetoun-falls | 0/2 | 0.795 | 24.4 |
| outdoor | 48x64 | 04-rocket, 10-hopetoun-falls | 0/2 | 0.795 | 24.4 |
| indoor | 24x32 | 03-coffee | 1/1 | 0.898 | 22.3 |
| indoor | 36x48 | 03-coffee | 1/1 | 0.900 | 22.1 |
| indoor | 48x64 | 03-coffee | 1/1 | 0.905 | 21.9 |
| cluttered | 24x32 | 11-shibuya-crossing | 0/1 | 0.684 | 19.0 |
| cluttered | 36x48 | 11-shibuya-crossing | 0/1 | 0.704 | 19.6 |
| cluttered | 48x64 | 11-shibuya-crossing | 0/1 | 0.721 | 19.6 |

## Palette usage (average then snap)

| density | avg distinct crayons per picture | avg share of cells in top 3 crayons | crayons never used across all pictures | avg crayons unused per picture |
|---|---|---|---|---|
| 24x32 | 7.8 | 83.1% | 3 of 24 | 16.2 |
| 36x48 | 8.3 | 82.5% | 1 of 24 | 15.7 |
| 48x64 | 8.6 | 82.2% | 1 of 24 | 15.4 |

- 24x32 crayons never used on any picture: Carnation Pink, Violet Red, Scarlet
- 36x48 crayons never used on any picture: Scarlet
- 48x64 crayons never used on any picture: Scarlet

## Blank-sheet privacy

- 24x32: number-free blank grids of all 11 images are byte-identical (same cell geometry); pixels are only white and one grid gray: yes; sheets are grayscale (no colors): yes. Cells are uniform squares; there are no outlines of the subject and no shading.
- 36x48: number-free blank grids of all 11 images are byte-identical (same cell geometry); pixels are only white and one grid gray: yes; sheets are grayscale (no colors): yes. Cells are uniform squares; there are no outlines of the subject and no shading.
- 48x64: number-free blank grids of all 11 images are byte-identical (same cell geometry); pixels are only white and one grid gray: yes; sheets are grayscale (no colors): yes. Cells are uniform squares; there are no outlines of the subject and no shading.

Leak measured as the share of adjacent cell pairs (left-right and up-down) holding the same number. The shuffled column is the same numbers placed in random cells (the share with no spatial structure).

| density | avg adjacent-same share | avg shuffled share | ratio |
|---|---|---|---|
| 24x32 | 75.8% | 37.6% | 2.0x |
| 36x48 | 78.8% | 36.5% | 2.2x |
| 48x64 | 80.6% | 35.9% | 2.2x |

### Three example sheets

![blank 01-astronaut](picture-method/average-then-snap/01-astronaut_36x48_blank.png)

![blank 02-chelsea-cat](picture-method/average-then-snap/02-chelsea-cat_36x48_blank.png)

![blank 11-shibuya-crossing](picture-method/average-then-snap/11-shibuya-crossing_36x48_blank.png)

| image | density | blank sheet | adjacent-same share | shuffled share |
|---|---|---|---|---|
| 01-astronaut | 36x48 | [picture-method/average-then-snap/01-astronaut_36x48_blank.png](picture-method/average-then-snap/01-astronaut_36x48_blank.png) | 66.7% | 16.2% |
| 02-chelsea-cat | 36x48 | [picture-method/average-then-snap/02-chelsea-cat_36x48_blank.png](picture-method/average-then-snap/02-chelsea-cat_36x48_blank.png) | 92.7% | 82.5% |
| 11-shibuya-crossing | 36x48 | [picture-method/average-then-snap/11-shibuya-crossing_36x48_blank.png](picture-method/average-then-snap/11-shibuya-crossing_36x48_blank.png) | 66.5% | 23.8% |

Can the subject be guessed from the numbers alone? **Not tested by a person or model.** What the numbers show: adjacent cells repeat the same number far more often than chance (ratios above), so runs and blobs of equal numbers trace the large shapes in the picture (backgrounds, faces, sky). Outlines of a subject can be inferred from where numbers change, but the colors cannot, and the identity of a subject has to be guessed from blob shapes. Treat the sheet as leaking shape, not identity.

## Practicality for a child

An island is a cell whose every existing up/down/left/right neighbour has a different number. Run length is the average number of consecutive same-numbered cells along a row (all cells / all runs).

| density | cells | avg islands per picture | islands per 100 cells | avg row run length |
|---|---|---|---|---|
| 24x32 | 768 | 26.3 | 3.42 | 4.20 |
| 36x48 | 1728 | 50.2 | 2.90 | 4.78 |
| 48x64 | 3072 | 76.1 | 2.48 | 5.24 |

Per image:

| image | density | islands | row run length |
|---|---|---|---|
| 01-astronaut | 24x32 | 65 | 2.23 |
| 01-astronaut | 36x48 | 98 | 2.72 |
| 01-astronaut | 48x64 | 122 | 3.06 |
| 02-chelsea-cat | 24x32 | 5 | 8.73 |
| 02-chelsea-cat | 36x48 | 16 | 9.49 |
| 02-chelsea-cat | 48x64 | 25 | 9.81 |
| 03-coffee | 24x32 | 35 | 2.97 |
| 03-coffee | 36x48 | 82 | 3.66 |
| 03-coffee | 48x64 | 120 | 4.36 |
| 04-rocket | 24x32 | 13 | 3.82 |
| 04-rocket | 36x48 | 27 | 4.73 |
| 04-rocket | 48x64 | 42 | 5.55 |
| 05-raccoon | 24x32 | 28 | 3.73 |
| 05-raccoon | 36x48 | 59 | 4.21 |
| 05-raccoon | 48x64 | 99 | 4.54 |
| 06-mona-lisa | 24x32 | 20 | 3.66 |
| 06-mona-lisa | 36x48 | 37 | 4.60 |
| 06-mona-lisa | 48x64 | 50 | 5.44 |
| 07-migrant-mother | 24x32 | 8 | 5.82 |
| 07-migrant-mother | 36x48 | 12 | 6.65 |
| 07-migrant-mother | 48x64 | 21 | 7.42 |
| 08-lunch-atop-skyscraper | 24x32 | 18 | 4.17 |
| 08-lunch-atop-skyscraper | 36x48 | 28 | 4.42 |
| 08-lunch-atop-skyscraper | 48x64 | 41 | 4.38 |
| 09-golden-retriever | 24x32 | 25 | 4.57 |
| 09-golden-retriever | 36x48 | 45 | 5.08 |
| 09-golden-retriever | 48x64 | 79 | 5.31 |
| 10-hopetoun-falls | 24x32 | 23 | 3.75 |
| 10-hopetoun-falls | 36x48 | 47 | 4.16 |
| 10-hopetoun-falls | 48x64 | 82 | 4.78 |
| 11-shibuya-crossing | 24x32 | 49 | 2.72 |
| 11-shibuya-crossing | 36x48 | 101 | 2.90 |
| 11-shibuya-crossing | 48x64 | 156 | 3.04 |

## Runtime

Median of 3 runs of boost + cell averaging + Lab snapping on the already-cropped picture, in ms (excludes file loading, cropping, rendering and metrics).

| density | avg ms per image |
|---|---|
| 24x32 | 90.5 |
| 36x48 | 85.9 |
| 48x64 | 93.1 |

Per image:

| image | density | ms |
|---|---|---|
| 01-astronaut | 24x32 | 9.2 |
| 01-astronaut | 36x48 | 12.9 |
| 01-astronaut | 48x64 | 15.2 |
| 02-chelsea-cat | 24x32 | 8.8 |
| 02-chelsea-cat | 36x48 | 7.8 |
| 02-chelsea-cat | 48x64 | 11.0 |
| 03-coffee | 24x32 | 6.4 |
| 03-coffee | 36x48 | 8.2 |
| 03-coffee | 48x64 | 15.9 |
| 04-rocket | 24x32 | 6.8 |
| 04-rocket | 36x48 | 10.1 |
| 04-rocket | 48x64 | 15.7 |
| 05-raccoon | 24x32 | 19.9 |
| 05-raccoon | 36x48 | 22.3 |
| 05-raccoon | 48x64 | 33.0 |
| 06-mona-lisa | 24x32 | 422.3 |
| 06-mona-lisa | 36x48 | 373.2 |
| 06-mona-lisa | 48x64 | 406.8 |
| 07-migrant-mother | 24x32 | 346.8 |
| 07-migrant-mother | 36x48 | 332.2 |
| 07-migrant-mother | 48x64 | 337.6 |
| 08-lunch-atop-skyscraper | 24x32 | 64.8 |
| 08-lunch-atop-skyscraper | 36x48 | 66.1 |
| 08-lunch-atop-skyscraper | 48x64 | 68.1 |
| 09-golden-retriever | 24x32 | 18.3 |
| 09-golden-retriever | 36x48 | 18.8 |
| 09-golden-retriever | 48x64 | 21.3 |
| 10-hopetoun-falls | 24x32 | 49.2 |
| 10-hopetoun-falls | 36x48 | 43.8 |
| 10-hopetoun-falls | 48x64 | 53.5 |
| 11-shibuya-crossing | 24x32 | 42.8 |
| 11-shibuya-crossing | 36x48 | 49.5 |
| 11-shibuya-crossing | 48x64 | 46.2 |

## Verdict

Rule used: the density with the most recognizable (proxy) pictures; ties go to the one with the fewest cells (least coloring for a child).

| density | recognizable (proxy) | mean L correlation |
|---|---|---|
| 24x32 | 4/11 | 0.811 |
| 36x48 | 4/11 | 0.820 |
| 48x64 | 4/11 | 0.827 |

Best density by that rule: **24x32**. Higher density keeps more detail (higher correlation) but costs more cells and more single-cell islands; see the practicality table before choosing.

Failure cases (proxy):
- 02-chelsea-cat at 24x32: light/dark structure lost (L correlation 0.60 < 0.85)
- 02-chelsea-cat at 36x48: light/dark structure lost (L correlation 0.63 < 0.85)
- 02-chelsea-cat at 48x64: light/dark structure lost (L correlation 0.65 < 0.85)
- 04-rocket at 24x32: light/dark structure lost (L correlation 0.75 < 0.85)
- 04-rocket at 36x48: light/dark structure lost (L correlation 0.75 < 0.85)
- 04-rocket at 48x64: light/dark structure lost (L correlation 0.74 < 0.85)
- 07-migrant-mother at 24x32: light/dark structure lost (L correlation 0.83 < 0.85); only 3 crayons used
- 07-migrant-mother at 36x48: light/dark structure lost (L correlation 0.84 < 0.85); only 3 crayons used
- 07-migrant-mother at 48x64: light/dark structure lost (L correlation 0.85 < 0.85); only 3 crayons used
- 08-lunch-atop-skyscraper at 24x32: light/dark structure lost (L correlation 0.82 < 0.85); only 3 crayons used
- 08-lunch-atop-skyscraper at 36x48: light/dark structure lost (L correlation 0.83 < 0.85); only 3 crayons used
- 08-lunch-atop-skyscraper at 48x64: light/dark structure lost (L correlation 0.84 < 0.85); only 3 crayons used
- 09-golden-retriever at 24x32: light/dark structure lost (L correlation 0.82 < 0.85)
- 09-golden-retriever at 36x48: light/dark structure lost (L correlation 0.82 < 0.85)
- 09-golden-retriever at 48x64: light/dark structure lost (L correlation 0.82 < 0.85)
- 10-hopetoun-falls at 24x32: light/dark structure lost (L correlation 0.83 < 0.85)
- 10-hopetoun-falls at 36x48: light/dark structure lost (L correlation 0.84 < 0.85)
- 10-hopetoun-falls at 48x64: light/dark structure lost (L correlation 0.85 < 0.85)
- 11-shibuya-crossing at 24x32: light/dark structure lost (L correlation 0.68 < 0.85)
- 11-shibuya-crossing at 36x48: light/dark structure lost (L correlation 0.70 < 0.85)
- 11-shibuya-crossing at 48x64: light/dark structure lost (L correlation 0.72 < 0.85)

Lowest light/dark correlation at the best density: 02-chelsea-cat (0.599), 11-shibuya-crossing (0.684).
