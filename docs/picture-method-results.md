# Picture method results: quantize then majority vote

Generated 2026-10-08 20:11 UTC by `python run_picture_method.py`.

## What was read

- Images read: **11** (expected 11).

| # | file | category | source | license | fetched size | original size | SHA-256 (file) | SHA-256 (decoded RGB) | crop to 3:4 |
|---|---|---|---|---|---|---|---|---|---|
| 01 | photos/01-astronaut.jpg | portrait | skimage.data.astronaut() | bundled sample; licence per the library's data docs (not verified at run time) | 512x512 | 512x512 | `011901a3f9084e22497e2b27642b44a39e8965c4c2febc5ddf2c3ccf298c8787` | `a8c429c18afa7b0fd5673e598d73a21225d94c864a71bbb3885126fdecb41071` | landscape/wide source: crop removes the sides (25% of the width) |
| 02 | photos/02-chelsea-cat.jpg | pet or animal | skimage.data.chelsea() | bundled sample; licence per the library's data docs (not verified at run time) | 451x300 | 451x300 | `e8605ae62ddd946bef56bba73435937edcab675f8ef20cdcee29fdbf2d94045f` | `416b729128bfb2c3d1eb69bf9b1734a796293abc17939267b2dc94f8a5784031` | landscape/wide source: crop removes the sides (50% of the width) |
| 03 | photos/03-coffee.jpg | indoor | skimage.data.coffee() | bundled sample; licence per the library's data docs (not verified at run time) | 600x400 | 600x400 | `80e2b46bbd310f215a6381ceac2ef7a403c23874ec48b3637cd74177e31ed4ea` | `0ce2b51640b9c95f19617f03eabf40c3f0368589cc1ee1190b70966165ac184f` | landscape/wide source: crop removes the sides (50% of the width) |
| 04 | photos/04-rocket.jpg | outdoor | skimage.data.rocket() | bundled sample; licence per the library's data docs (not verified at run time) | 640x427 | 640x427 | `2d3d62a61bf417fd93253df812c357b86fdfcd50d74b4280ae252455fe7064db` | `3d4435cc745752b7f9724df88c6e18817de3ce7e3d2d71c55f85f7831e68f197` | landscape/wide source: crop removes the sides (50% of the width) |
| 05 | photos/05-raccoon.jpg | pet or animal | scipy.datasets.face() | bundled sample; licence per the library's data docs (not verified at run time) | 1024x768 | 1024x768 | `1324d7414eec1ec09bbe1998f78a4c1854fd6baec9a1e09286232cab5dd26a17` | `9f16f4e284d28f4b8e0356171bc6543d2a0d24a0bd55dabebbd30e102aa8946c` | landscape/wide source: crop removes the sides (44% of the width) |
| 06 | photos/06-mona-lisa.jpg | portrait | Wikimedia Commons File:Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg (Special:FilePath, width=1600) | Public domain | 1920x2861 | 7479x11146 | `276868845c54914913c965b208eec75db55c1675489e563852f155c5db58b536` | `0df09ed891080d91637ce2ef582117c2f93331beb33eecb33993a2df24d720ec` | taller than 3:4: crop removes top and bottom (11% of the height) |
| 07 | photos/07-migrant-mother.jpg | group | Wikimedia Commons File:Lange-MigrantMother02.jpg (Special:FilePath, width=1600) | Public domain | 1920x2496 | 6205x8066 | `e6657df96f6dadede759d88c6c3ebc14dc956633c246a3a1046a47ebf5c17afd` | `70c1b51a464f3f1c920225a90ae4869e89f93acb5d0d099b9e2dd9ce99191ca0` | landscape/wide source: crop removes the sides (3% of the width) |
| 08 | photos/08-lunch-atop-skyscraper.jpg | group | Wikimedia Commons File:Lunch atop a Skyscraper.jpg (Special:FilePath, width=1600) | Public domain | 1920x1482 | 8192x6322 | `3a487894b9c1462dbe0813ffb1c82d8e0508b440337cee1a3ef34a683e559b1f` | `eddb8164b8fd169c27fd99edabf1a261dc7fcc08b7a8bc590fa7e04a9fce3628` | landscape/wide source: crop removes the sides (42% of the width) |
| 09 | photos/09-golden-retriever.jpg | pet or animal | Wikimedia Commons File:Golden Retriever Dukedestiny01.jpg (Special:FilePath, width=1600) | Public domain | 1024x768 | 1024x768 | `7a7d156fcb6fe815670924619cf4bb2e310232a93e6b7fea64505d1dac486ec5` | `dd231c82158e6a7b72ac90a2ab1b60f75e233dcf66c13e33c2c0ae713d589157` | landscape/wide source: crop removes the sides (44% of the width) |
| 10 | photos/10-hopetoun-falls.jpg | outdoor | Wikimedia Commons File:Hopetoun falls.jpg (Special:FilePath, width=1600) | CC BY-SA 3.0 | 1920x1280 | 3072x2048 | `afc9ddf298d06298520e981f5b7fb7d9c89a6de68e8bd8363091c59405cc7fcd` | `b957f5a0730ef41c95a4468d25a9ec4a8e5aafff854b8e00d9ad80320ffc5fcc` | landscape/wide source: crop removes the sides (50% of the width) |
| 11 | photos/11-shibuya-crossing.jpg | cluttered | Wikimedia Commons File:Tokyo Shibuya Scramble Crossing 2018-10-09.jpg (Special:FilePath, width=1600) | CC BY-SA 2.0 | 1920x1280 | 5853x3902 | `615151cfc947a72008a1d8aa12ba606d437bcc5d656ff87305228e094f916edd` | `cf480e2aba1960b0592b343b3b969ecdfb49b815f7cf9ebed9e4e77d09bae0e8` | landscape/wide source: crop removes the sides (50% of the width) |

Bundled images are re-encoded to JPEG (quality 95) when saved, so their file hash depends on the Pillow build; the decoded-RGB hash is of the library's original array and is the one to compare.

### Palette: Crayola 24-count box

| # | crayon | hex |
|---|---|---|
| 1 | Red | #EE204D |
| 2 | Yellow | #FCE883 |
| 3 | Blue | #1F75FE |
| 4 | Brown | #B5674D |
| 5 | Orange | #FF7538 |
| 6 | Green | #1CAC78 |
| 7 | Violet | #926EAE |
| 8 | Black | #232323 |
| 9 | Carnation Pink | #FFAACC |
| 10 | Yellow Green | #C5E384 |
| 11 | Blue Green | #0D98BA |
| 12 | Red Orange | #FF5349 |
| 13 | Red Violet | #C0448F |
| 14 | White | #EDEDED |
| 15 | Gray | #95918C |
| 16 | Yellow Orange | #FFAE42 |
| 17 | Blue Violet | #7366BD |
| 18 | Apricot | #FDD9B5 |
| 19 | Scarlet | #FC2847 |
| 20 | Tan | #FAA76C |
| 21 | Sky Blue | #80DAEB |
| 22 | Peach | #FFCBA4 |
| 23 | Orchid | #E6A8D7 |
| 24 | Burnt Sienna | #EA7E5D |

Cell numbers are these 1-24 indexes.

### Densities (columns x rows): 24x32, 36x48, 48x64

### Method

Pre-processing: center-crop to 3:4 portrait, then Lanczos-resize to (cols x 6) by (rows x 6) pixels, i.e. 6x6 pixels per cell.
1. Quantize: every pixel of that small image is mapped to the nearest of the 24 crayons (Euclidean distance in CIE Lab, D65).
2. Vote: each cell takes the crayon most common among its pixels. A tie goes to the tied crayon with the larger pixel share in the 8 neighboring cells; a remaining tie goes to the lower palette number.
3. Alternative (reported separately): Floyd-Steinberg dithering in Lab during step 1, then the same vote.
Previews and sheets are in `docs/picture-method/quantize-vote/`. Main results below are WITHOUT dithering.

## Per image and density

Original (3:4 crop), colored preview, blank numbered grid. Recognizability is a computed proxy (see next section).

### 01 astronaut (portrait)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/01-astronaut_original.png) | ![](picture-method/quantize-vote/01-astronaut_24x32_preview.png) | ![](picture-method/quantize-vote/01-astronaut_24x32_blank.png) | 61 ms | recognizable |
| 36x48 | ![](picture-method/quantize-vote/01-astronaut_original.png) | ![](picture-method/quantize-vote/01-astronaut_36x48_preview.png) | ![](picture-method/quantize-vote/01-astronaut_36x48_blank.png) | 104 ms | recognizable |
| 48x64 | ![](picture-method/quantize-vote/01-astronaut_original.png) | ![](picture-method/quantize-vote/01-astronaut_48x64_preview.png) | ![](picture-method/quantize-vote/01-astronaut_48x64_blank.png) | 196 ms | recognizable |

### 02 chelsea-cat (pet or animal)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/02-chelsea-cat_original.png) | ![](picture-method/quantize-vote/02-chelsea-cat_24x32_preview.png) | ![](picture-method/quantize-vote/02-chelsea-cat_24x32_blank.png) | 45 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.72); only 5 crayons survive the vote; top 3 crayons fill 98% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/02-chelsea-cat_original.png) | ![](picture-method/quantize-vote/02-chelsea-cat_36x48_preview.png) | ![](picture-method/quantize-vote/02-chelsea-cat_36x48_blank.png) | 110 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.74); only 5 crayons survive the vote; top 3 crayons fill 98% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/02-chelsea-cat_original.png) | ![](picture-method/quantize-vote/02-chelsea-cat_48x64_preview.png) | ![](picture-method/quantize-vote/02-chelsea-cat_48x64_blank.png) | 185 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.76); only 5 crayons survive the vote; top 3 crayons fill 97% of cells (detail lost) |

### 03 coffee (indoor)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/03-coffee_original.png) | ![](picture-method/quantize-vote/03-coffee_24x32_preview.png) | ![](picture-method/quantize-vote/03-coffee_24x32_blank.png) | 44 ms | recognizable |
| 36x48 | ![](picture-method/quantize-vote/03-coffee_original.png) | ![](picture-method/quantize-vote/03-coffee_36x48_preview.png) | ![](picture-method/quantize-vote/03-coffee_36x48_blank.png) | 102 ms | recognizable |
| 48x64 | ![](picture-method/quantize-vote/03-coffee_original.png) | ![](picture-method/quantize-vote/03-coffee_48x64_preview.png) | ![](picture-method/quantize-vote/03-coffee_48x64_blank.png) | 190 ms | recognizable |

### 04 rocket (outdoor)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/04-rocket_original.png) | ![](picture-method/quantize-vote/04-rocket_24x32_preview.png) | ![](picture-method/quantize-vote/04-rocket_24x32_blank.png) | 48 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.82); top 3 crayons fill 94% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/04-rocket_original.png) | ![](picture-method/quantize-vote/04-rocket_36x48_preview.png) | ![](picture-method/quantize-vote/04-rocket_36x48_blank.png) | 121 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.82); top 3 crayons fill 95% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/04-rocket_original.png) | ![](picture-method/quantize-vote/04-rocket_48x64_preview.png) | ![](picture-method/quantize-vote/04-rocket_48x64_blank.png) | 269 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.81); top 3 crayons fill 95% of cells (detail lost) |

### 05 raccoon (pet or animal)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/05-raccoon_original.png) | ![](picture-method/quantize-vote/05-raccoon_24x32_preview.png) | ![](picture-method/quantize-vote/05-raccoon_24x32_blank.png) | 71 ms | partly recognizable: only 5 crayons survive the vote; top 3 crayons fill 87% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/05-raccoon_original.png) | ![](picture-method/quantize-vote/05-raccoon_36x48_preview.png) | ![](picture-method/quantize-vote/05-raccoon_36x48_blank.png) | 141 ms | partly recognizable: top 3 crayons fill 87% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/05-raccoon_original.png) | ![](picture-method/quantize-vote/05-raccoon_48x64_preview.png) | ![](picture-method/quantize-vote/05-raccoon_48x64_blank.png) | 215 ms | partly recognizable: top 3 crayons fill 87% of cells (detail lost) |

### 06 mona-lisa (portrait)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/06-mona-lisa_original.png) | ![](picture-method/quantize-vote/06-mona-lisa_24x32_preview.png) | ![](picture-method/quantize-vote/06-mona-lisa_24x32_blank.png) | 127 ms | partly recognizable: top 3 crayons fill 92% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/06-mona-lisa_original.png) | ![](picture-method/quantize-vote/06-mona-lisa_36x48_preview.png) | ![](picture-method/quantize-vote/06-mona-lisa_36x48_blank.png) | 197 ms | partly recognizable: top 3 crayons fill 91% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/06-mona-lisa_original.png) | ![](picture-method/quantize-vote/06-mona-lisa_48x64_preview.png) | ![](picture-method/quantize-vote/06-mona-lisa_48x64_blank.png) | 274 ms | partly recognizable: top 3 crayons fill 91% of cells (detail lost) |

### 07 migrant-mother (group)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/07-migrant-mother_original.png) | ![](picture-method/quantize-vote/07-migrant-mother_24x32_preview.png) | ![](picture-method/quantize-vote/07-migrant-mother_24x32_blank.png) | 119 ms | partly recognizable: only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/07-migrant-mother_original.png) | ![](picture-method/quantize-vote/07-migrant-mother_36x48_preview.png) | ![](picture-method/quantize-vote/07-migrant-mother_36x48_blank.png) | 177 ms | partly recognizable: only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/07-migrant-mother_original.png) | ![](picture-method/quantize-vote/07-migrant-mother_48x64_preview.png) | ![](picture-method/quantize-vote/07-migrant-mother_48x64_blank.png) | 275 ms | partly recognizable: only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost) |

### 08 lunch-atop-skyscraper (group)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_original.png) | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_24x32_preview.png) | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_24x32_blank.png) | 75 ms | partly recognizable: only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_original.png) | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_36x48_preview.png) | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_36x48_blank.png) | 131 ms | partly recognizable: only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_original.png) | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_48x64_preview.png) | ![](picture-method/quantize-vote/08-lunch-atop-skyscraper_48x64_blank.png) | 256 ms | partly recognizable: only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost) |

### 09 golden-retriever (pet or animal)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/09-golden-retriever_original.png) | ![](picture-method/quantize-vote/09-golden-retriever_24x32_preview.png) | ![](picture-method/quantize-vote/09-golden-retriever_24x32_blank.png) | 49 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.84) |
| 36x48 | ![](picture-method/quantize-vote/09-golden-retriever_original.png) | ![](picture-method/quantize-vote/09-golden-retriever_36x48_preview.png) | ![](picture-method/quantize-vote/09-golden-retriever_36x48_blank.png) | 107 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.85) |
| 48x64 | ![](picture-method/quantize-vote/09-golden-retriever_original.png) | ![](picture-method/quantize-vote/09-golden-retriever_48x64_preview.png) | ![](picture-method/quantize-vote/09-golden-retriever_48x64_blank.png) | 194 ms | recognizable |

### 10 hopetoun-falls (outdoor)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/10-hopetoun-falls_original.png) | ![](picture-method/quantize-vote/10-hopetoun-falls_24x32_preview.png) | ![](picture-method/quantize-vote/10-hopetoun-falls_24x32_blank.png) | 74 ms | partly recognizable: only 5 crayons survive the vote; top 3 crayons fill 99% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/10-hopetoun-falls_original.png) | ![](picture-method/quantize-vote/10-hopetoun-falls_36x48_preview.png) | ![](picture-method/quantize-vote/10-hopetoun-falls_36x48_blank.png) | 123 ms | partly recognizable: top 3 crayons fill 99% of cells (detail lost) |
| 48x64 | ![](picture-method/quantize-vote/10-hopetoun-falls_original.png) | ![](picture-method/quantize-vote/10-hopetoun-falls_48x64_preview.png) | ![](picture-method/quantize-vote/10-hopetoun-falls_48x64_blank.png) | 220 ms | partly recognizable: top 3 crayons fill 99% of cells (detail lost) |

### 11 shibuya-crossing (cluttered)

| density | original | preview | blank grid | runtime | recognizability |
|---|---|---|---|---|---|
| 24x32 | ![](picture-method/quantize-vote/11-shibuya-crossing_original.png) | ![](picture-method/quantize-vote/11-shibuya-crossing_24x32_preview.png) | ![](picture-method/quantize-vote/11-shibuya-crossing_24x32_blank.png) | 62 ms | not recognizable: light/dark structure only partly kept (lightness r=0.67); top 3 crayons fill 87% of cells (detail lost) |
| 36x48 | ![](picture-method/quantize-vote/11-shibuya-crossing_original.png) | ![](picture-method/quantize-vote/11-shibuya-crossing_36x48_preview.png) | ![](picture-method/quantize-vote/11-shibuya-crossing_36x48_blank.png) | 121 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.70) |
| 48x64 | ![](picture-method/quantize-vote/11-shibuya-crossing_original.png) | ![](picture-method/quantize-vote/11-shibuya-crossing_48x64_preview.png) | ![](picture-method/quantize-vote/11-shibuya-crossing_48x64_blank.png) | 226 ms | partly recognizable: light/dark structure only partly kept (lightness r=0.72) |

## Contact sheets (all 11 images, pinned order, 4 per row)

### 24x32

![](picture-method/quantize-vote/contact_24x32.png)

### 36x48

![](picture-method/quantize-vote/contact_36x48.png)

### 48x64

![](picture-method/quantize-vote/contact_48x64.png)

## Recognizability notes

Computed, not eyeballed: the verdict uses the correlation of preview lightness with the original's cell lightness (>=0.85 recognizable, >=0.70 partly) and flags speckle (>8% single-cell islands), <=5 crayons, or top-3 crayons >85% of cells. Treat as a screening proxy and check the contact sheets by eye.

### By category

| category | 24x32 | 36x48 | 48x64 |
|---|---|---|---|
| portrait | 1 recognizable, 1 partly recognizable; lightness r 0.90 | 1 recognizable, 1 partly recognizable; lightness r 0.91 | 1 recognizable, 1 partly recognizable; lightness r 0.91 |
| group | 2 partly recognizable; lightness r 0.87 | 2 partly recognizable; lightness r 0.87 | 2 partly recognizable; lightness r 0.88 |
| pet or animal | 3 partly recognizable; lightness r 0.80 | 3 partly recognizable; lightness r 0.82 | 2 partly recognizable, 1 recognizable; lightness r 0.82 |
| outdoor | 2 partly recognizable; lightness r 0.85 | 2 partly recognizable; lightness r 0.85 | 2 partly recognizable; lightness r 0.85 |
| indoor | 1 recognizable; lightness r 0.93 | 1 recognizable; lightness r 0.93 | 1 recognizable; lightness r 0.93 |
| cluttered | 1 not recognizable; lightness r 0.67 | 1 partly recognizable; lightness r 0.70 | 1 partly recognizable; lightness r 0.72 |

### Per image

| image | 24x32 | 36x48 | 48x64 |
|---|---|---|---|
| 01 astronaut | recognizable, r=0.90, dE=15.7 | recognizable, r=0.91, dE=15.4 | recognizable, r=0.92, dE=14.9 |
| 02 chelsea-cat | partly recognizable (light/dark structure only partly kept (lightness r=0.72); only 5 crayons survive the vote; top 3 crayons fill 98% of cells (detail lost)), r=0.72, dE=18.9 | partly recognizable (light/dark structure only partly kept (lightness r=0.74); only 5 crayons survive the vote; top 3 crayons fill 98% of cells (detail lost)), r=0.74, dE=18.9 | partly recognizable (light/dark structure only partly kept (lightness r=0.76); only 5 crayons survive the vote; top 3 crayons fill 97% of cells (detail lost)), r=0.76, dE=18.9 |
| 03 coffee | recognizable, r=0.93, dE=20.5 | recognizable, r=0.93, dE=20.0 | recognizable, r=0.93, dE=19.6 |
| 04 rocket | partly recognizable (light/dark structure only partly kept (lightness r=0.82); top 3 crayons fill 94% of cells (detail lost)), r=0.82, dE=23.2 | partly recognizable (light/dark structure only partly kept (lightness r=0.82); top 3 crayons fill 95% of cells (detail lost)), r=0.82, dE=22.9 | partly recognizable (light/dark structure only partly kept (lightness r=0.81); top 3 crayons fill 95% of cells (detail lost)), r=0.81, dE=22.9 |
| 05 raccoon | partly recognizable (only 5 crayons survive the vote; top 3 crayons fill 87% of cells (detail lost)), r=0.85, dE=18.0 | partly recognizable (top 3 crayons fill 87% of cells (detail lost)), r=0.86, dE=17.9 | partly recognizable (top 3 crayons fill 87% of cells (detail lost)), r=0.87, dE=17.9 |
| 06 mona-lisa | partly recognizable (top 3 crayons fill 92% of cells (detail lost)), r=0.89, dE=19.8 | partly recognizable (top 3 crayons fill 91% of cells (detail lost)), r=0.90, dE=19.6 | partly recognizable (top 3 crayons fill 91% of cells (detail lost)), r=0.90, dE=19.6 |
| 07 migrant-mother | partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost)), r=0.86, dE=11.0 | partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost)), r=0.87, dE=10.9 | partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost)), r=0.87, dE=10.9 |
| 08 lunch-atop-skyscraper | partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost)), r=0.87, dE=13.4 | partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost)), r=0.88, dE=13.1 | partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost)), r=0.88, dE=12.8 |
| 09 golden-retriever | partly recognizable (light/dark structure only partly kept (lightness r=0.84)), r=0.84, dE=18.8 | partly recognizable (light/dark structure only partly kept (lightness r=0.85)), r=0.85, dE=18.8 | recognizable, r=0.85, dE=18.6 |
| 10 hopetoun-falls | partly recognizable (only 5 crayons survive the vote; top 3 crayons fill 99% of cells (detail lost)), r=0.88, dE=16.4 | partly recognizable (top 3 crayons fill 99% of cells (detail lost)), r=0.88, dE=16.2 | partly recognizable (top 3 crayons fill 99% of cells (detail lost)), r=0.88, dE=16.0 |
| 11 shibuya-crossing | not recognizable (light/dark structure only partly kept (lightness r=0.67); top 3 crayons fill 87% of cells (detail lost)), r=0.67, dE=18.7 | partly recognizable (light/dark structure only partly kept (lightness r=0.70)), r=0.70, dE=19.0 | partly recognizable (light/dark structure only partly kept (lightness r=0.72)), r=0.72, dE=19.1 |

## Palette usage

| density | avg distinct crayons per picture | avg share of cells in top 3 crayons | avg crayons unused per picture | crayons never used in any picture |
|---|---|---|---|---|
| 24x32 | 7.5 | 88% | 16.5 | 5 (Red, Carnation Pink, Red Violet, Scarlet, Sky Blue) |
| 36x48 | 8.1 | 88% | 15.9 | 3 (Red, Carnation Pink, Scarlet) |
| 48x64 | 8.4 | 87% | 15.6 | 3 (Red, Carnation Pink, Scarlet) |

## Blank-sheet privacy

- 24x32: 11/11 blank grids pass the geometry check (identical pixel size per density, grayscale only, the outer 2 px ring of every cell is pure white, so no outlines, grid lines or shading; only the digits differ).
- 36x48: 11/11 blank grids pass the geometry check (identical pixel size per density, grayscale only, the outer 2 px ring of every cell is pure white, so no outlines, grid lines or shading; only the digits differ).
- 48x64: 11/11 blank grids pass the geometry check (identical pixel size per density, grayscale only, the outer 2 px ring of every cell is pure white, so no outlines, grid lines or shading; only the digits differ).

Leak measure: share of horizontally/vertically adjacent cell pairs carrying the same number, against the share expected if the same numbers were scattered at random.

| density | adjacent same-number share | random-scatter baseline | ratio |
|---|---|---|---|
| 24x32 | 77% | 38% | 2.0x |
| 36x48 | 79% | 37% | 2.1x |
| 48x64 | 81% | 37% | 2.2x |

Can the subject be guessed from the numbers alone? Not tested by a person or model here. What is measured: the numbers form large same-number regions (ratio above), so shapes and light/dark layout are readable in the digits for anyone who looks for them; the digits do not name colors, so material, identity and color are not given away.

Example sheets (first 10 rows of the first density; full sheets are the blank PNGs):

01 astronaut (24x32), blank PNG: `docs/picture-method/quantize-vote/01-astronaut_24x32_blank.png`

```
15 15 15 15 15 15 15 14 14 15 15 14 14 14 14 14 14 14 14 14 15  4  8 15
15 15 15 15 15 15 14 14 15 15 18 15 14 14 14 14 14 14 14 14 14  4  8 15
15 15 15 15 14 14 14 15  8 15 15 15  4 15 14 14 14 14 14 14 14  4  8 15
15 15 15 15 15 15 15 15 15 15 15 15  4  8 14 14 14 14 15 14 14  4  4 14
15 15 15 15 15 15 15  4  4  4 15 15  8  8  8 14 14 14 15 14 14  4  4 14
15 15 15 15 15 15  4  8 18 18 18 18  8  8  8 14 14 14 15 14 14  8  8 14
15 15 15 15 15 15  8 18 18 18 15 15 15  8  8 15 15 14 14 14 14  8  8 14
15 15 15 15 15 14 14 18 18 22 15 18 15  8 14 14 14 14 14 14 14 15  8 15
15 15 15 15 14 14 14 15 18 22  4 22 15 14 14 14 14 14 14 14 14 15  8 15
15 15 14 15 14 14  8  8 18 18 15 18 14 14 14 14 14 14 14 14 14  8  8 15
```

02 chelsea-cat (24x32), blank PNG: `docs/picture-method/quantize-vote/02-chelsea-cat_24x32_blank.png`

```
 4  4  4  4  4  4  4  4  4  4 15  4  8  4  8  4  4  4  4  4  4  4 15 15
 4  4  4  4  4  4  4  4  4  4 15  4  8  4  4  4  4  8  4  4  4  4  4 15
 4  4  4  4  4  4  4  4  4  4 15  4  4  4  8  4  8  4  4  4  4  4  4 15
 4  4  4  4  4  4  4  4  4  4 15  4  8  4  4  4  4  4  4  4  4  4  4 15
 4  4  4  4  4  4  4  4  4  4 15  4  4  4  4  4  4  4  4  4  4  4  4  4
 4  4  4  4  4  4  4  4  4 15  4  4  4  4  4  4  4  4  8  4  4  4 15  4
 4  4  4  4  4  4  4  4  4  4  4  4  4 15  4  4  4  4  4 15  4 15 15  4
 4  4  4 15  4  4  4  4  4  4  4  4  4 15  4  4  4  4  4 15  4  4 15  4
 4  4 15 15  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4 15 15
 4  4  4  8  4  8  8  8  4  4  4  4  4  4  4  4  4  4  4  4 15  4 15 15
```

03 coffee (24x32), blank PNG: `docs/picture-method/quantize-vote/03-coffee_24x32_blank.png`

```
 4 24 24 24  4  4  4  4  4  4  4 24 24 24 24 24 24 24 24 24 24 24 24 24
24 24 24  4  4  4  4  4  4  4 14 14 14 24 24 24 24 24 24 24 24 24 24 24
24 24  4  4  4  4 14 14 14 18 18 18 18 14 14 14 24 24 24 24 24 24 24 24
 4  4  4  4  4 14 18 22 22 22 22 22 22 22 18 18 14 24 24 24 24 24 24 24
 4  4  4 14 14 18 20 20 22 22 22 22 22 22 22 22 18 14 14 24  4 24 24 24
 4  4  4 14 18 20 20 20 20 20 20 22 22 22 22 22 22 18 14  4  4  4 24 24
 4 24 14 18 20 20 20 20 20 20 20 20 20 20 22 22 22 22 18 14 22 22 24 24
12 12 14 18 20 20 20 20 20  4  4 20 20 20 20 20 22 22 22 14 22 22 24 24
12 12 14 20 20 20 24  4  4  4  4  4  4  4 20 20 20 22 22 14 14 24 24 24
12 12 14 20 20 24  4  4  4  4  4  4  4  4  4 24 20 20 22 14 14 12 24  4
```

## Practicality for a child

| density | cells | avg single-cell islands per picture | islands as share of cells | avg run length along a row (cells) |
|---|---|---|---|---|
| 24x32 | 768 | 23 | 3.0% | 3.96 |
| 36x48 | 1728 | 45 | 2.6% | 4.56 |
| 48x64 | 3072 | 71 | 2.3% | 5.06 |

An island is a cell whose every existing up/down/left/right neighbor has a different number.
Cells that needed the neighbor tie-break: 24x32 1.3%, 36x48 1.4%, 48x64 1.4%.

## Runtime (resize + quantize + vote, no image decoding; ms)

| image | 24x32 | 36x48 | 48x64 |
|---|---|---|---|
| 01 astronaut | 61 | 104 | 196 |
| 02 chelsea-cat | 45 | 110 | 185 |
| 03 coffee | 44 | 102 | 190 |
| 04 rocket | 48 | 121 | 269 |
| 05 raccoon | 71 | 141 | 215 |
| 06 mona-lisa | 127 | 197 | 274 |
| 07 migrant-mother | 119 | 177 | 275 |
| 08 lunch-atop-skyscraper | 75 | 131 | 256 |
| 09 golden-retriever | 49 | 107 | 194 |
| 10 hopetoun-falls | 74 | 123 | 220 |
| 11 shibuya-crossing | 62 | 121 | 226 |
| mean | 71 | 130 | 227 |

## Dithering comparison (Floyd-Steinberg in Lab vs none)

| density | metric | no dither | dither |
|---|---|---|---|
| 24x32 | lightness r | 0.840 | 0.790 |
| 24x32 | mean dE to original | 17.7 | 19.6 |
| 24x32 | island share | 3.0% | 4.1% |
| 24x32 | row run length | 3.96 | 3.88 |
| 24x32 | adjacent same-number | 76.5% | 74.3% |
| 24x32 | distinct crayons | 7.5 | 7.6 |
| 24x32 | runtime s | 0.07 | 0.76 |
| 36x48 | lightness r | 0.849 | 0.795 |
| 36x48 | mean dE to original | 17.5 | 19.6 |
| 36x48 | island share | 2.6% | 3.1% |
| 36x48 | row run length | 4.56 | 4.44 |
| 36x48 | adjacent same-number | 79.2% | 77.4% |
| 36x48 | distinct crayons | 8.1 | 8.3 |
| 36x48 | runtime s | 0.13 | 1.75 |
| 48x64 | lightness r | 0.854 | 0.799 |
| 48x64 | mean dE to original | 17.4 | 19.5 |
| 48x64 | island share | 2.3% | 2.7% |
| 48x64 | row run length | 5.06 | 5.02 |
| 48x64 | adjacent same-number | 80.9% | 79.2% |
| 48x64 | distinct crayons | 8.4 | 9.0 |
| 48x64 | runtime s | 0.23 | 3.13 |

- 24x32: dithering changes lightness r by -0.050 and island share by +1.1 points: hurts or is mixed (more speckle and/or lower correlation); the majority vote already averages tones within a cell.
- 36x48: dithering changes lightness r by -0.054 and island share by +0.6 points: hurts or is mixed (more speckle and/or lower correlation); the majority vote already averages tones within a cell.
- 48x64: dithering changes lightness r by -0.055 and island share by +0.4 points: hurts or is mixed (more speckle and/or lower correlation); the majority vote already averages tones within a cell.

## Verdict

Density score = mean lightness r minus 2 x mean island share (heuristic, stated so it can be challenged): 24x32 = 0.780, 36x48 = 0.797, 48x64 = 0.808. Best by this score: **48x64**. Finer grids keep more detail but cost the child more cells; the island and run-length tables show the trade.

Failure cases at 48x64:
- 02 chelsea-cat: partly recognizable (light/dark structure only partly kept (lightness r=0.76); only 5 crayons survive the vote; top 3 crayons fill 97% of cells (detail lost))
- 04 rocket: partly recognizable (light/dark structure only partly kept (lightness r=0.81); top 3 crayons fill 95% of cells (detail lost))
- 05 raccoon: partly recognizable (top 3 crayons fill 87% of cells (detail lost))
- 06 mona-lisa: partly recognizable (top 3 crayons fill 91% of cells (detail lost))
- 07 migrant-mother: partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost))
- 08 lunch-atop-skyscraper: partly recognizable (only 3 crayons survive the vote; top 3 crayons fill 100% of cells (detail lost))
- 10 hopetoun-falls: partly recognizable (top 3 crayons fill 99% of cells (detail lost))
- 11 shibuya-crossing: partly recognizable (light/dark structure only partly kept (lightness r=0.72))

Palette collapse (6 or fewer crayons used): 02 chelsea-cat @ 24x32, 02 chelsea-cat @ 36x48, 02 chelsea-cat @ 48x64, 05 raccoon @ 24x32, 05 raccoon @ 36x48, 05 raccoon @ 48x64, 07 migrant-mother @ 24x32, 07 migrant-mother @ 36x48, 07 migrant-mother @ 48x64, 08 lunch-atop-skyscraper @ 24x32, 08 lunch-atop-skyscraper @ 36x48, 08 lunch-atop-skyscraper @ 48x64, 09 golden-retriever @ 24x32, 09 golden-retriever @ 36x48, 09 golden-retriever @ 48x64, 10 hopetoun-falls @ 24x32

