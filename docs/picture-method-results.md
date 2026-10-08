# Picture method results: edge-aware cell coloring

Generated 2026-10-08 21:33 UTC (Python 3.12.15). Regenerate with `python -m picture_method`.

## What was read

- Images read: **11** (expected 11)
- Densities (columns x rows): 24x32, 36x48, 48x64
- Pre-processing: center-crop to 3:4 portrait (width:height), then resize to the grid (each cell analysed from a 8x8 pixel block, Lanczos).

### Images

| # | file | category | source | license | pixels | SHA-256 | crop / note |
|---|---|---|---|---|---|---|---|
| 1 | 01-astronaut.jpg | portrait | skimage.data.astronaut() | bundled with library (scikit-image / SciPy data; see library docs) | 512x512 | `011901a3f9084e22497e2b27642b44a39e8965c4c2febc5ddf2c3ccf298c8787` | square-ish source: crop removes the sides (128 px); re-encoded as JPEG q95 |
| 2 | 02-chelsea-cat.jpg | pet or animal | skimage.data.chelsea() | bundled with library (scikit-image / SciPy data; see library docs) | 451x300 | `e8605ae62ddd946bef56bba73435937edcab675f8ef20cdcee29fdbf2d94045f` | landscape source: crop removes the sides (226 px); re-encoded as JPEG q95 |
| 3 | 03-coffee.jpg | indoor | skimage.data.coffee() | bundled with library (scikit-image / SciPy data; see library docs) | 600x400 | `80e2b46bbd310f215a6381ceac2ef7a403c23874ec48b3637cd74177e31ed4ea` | landscape source: crop removes the sides (300 px); re-encoded as JPEG q95 |
| 4 | 04-rocket.jpg | outdoor | skimage.data.rocket() | bundled with library (scikit-image / SciPy data; see library docs) | 640x427 | `2d3d62a61bf417fd93253df812c357b86fdfcd50d74b4280ae252455fe7064db` | landscape source: crop removes the sides (320 px); re-encoded as JPEG q95 |
| 5 | 05-raccoon.jpg | pet or animal | scipy.datasets.face() | bundled with library (scikit-image / SciPy data; see library docs) | 1024x768 | `1324d7414eec1ec09bbe1998f78a4c1854fd6baec9a1e09286232cab5dd26a17` | landscape source: crop removes the sides (448 px); re-encoded as JPEG q95 |
| 6 | 06-mona-lisa.jpg | portrait | Wikimedia Commons File:Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg (Special:FilePath, width=1600) | Public domain | 1920x2861 | `276868845c54914913c965b208eec75db55c1675489e563852f155c5db58b536` | taller than 3:4: crop removes top and bottom (301 px) |
| 7 | 07-migrant-mother.jpg | group | Wikimedia Commons File:Lange-MigrantMother02.jpg (Special:FilePath, width=1600) | Public domain | 1920x2496 | `e6657df96f6dadede759d88c6c3ebc14dc956633c246a3a1046a47ebf5c17afd` | square-ish source: crop removes the sides (48 px) |
| 8 | 08-lunch-atop-skyscraper.jpg | group | Wikimedia Commons File:Lunch atop a Skyscraper.jpg (Special:FilePath, width=1600) | Public domain | 1920x1482 | `3a487894b9c1462dbe0813ffb1c82d8e0508b440337cee1a3ef34a683e559b1f` | landscape source: crop removes the sides (808 px) |
| 9 | 09-golden-retriever.jpg | pet or animal | Wikimedia Commons File:Golden Retriever Dukedestiny01.jpg (Special:FilePath, width=1600) | Public domain | 1024x768 | `7a7d156fcb6fe815670924619cf4bb2e310232a93e6b7fea64505d1dac486ec5` | landscape source: crop removes the sides (448 px) |
| 10 | 10-hopetoun-falls.jpg | outdoor | Wikimedia Commons File:Hopetoun falls.jpg (Special:FilePath, width=1600) | CC BY-SA 3.0 | 1920x1280 | `afc9ddf298d06298520e981f5b7fb7d9c89a6de68e8bd8363091c59405cc7fcd` | landscape source: crop removes the sides (960 px) |
| 11 | 11-shibuya-crossing.jpg | cluttered | Wikimedia Commons File:Tokyo Shibuya Scramble Crossing 2018-10-09.jpg (Special:FilePath, width=1600) | CC BY-SA 2.0 | 1920x1280 | `615151cfc947a72008a1d8aa12ba606d437bcc5d656ff87305228e094f916edd` | landscape source: crop removes the sides (960 px) |

### Palette: Crayola 24-count (cell number = index)

| # | name | hex |
|---|---|---|
| 1 | Red | #ED0A3F |
| 2 | Red-Orange | #FF681F |
| 3 | Orange | #FF8833 |
| 4 | Yellow-Orange | #FFAE42 |
| 5 | Yellow | #FBE870 |
| 6 | Yellow-Green | #C5E17A |
| 7 | Green | #01A638 |
| 8 | Blue-Green | #0D98BA |
| 9 | Blue | #0066FF |
| 10 | Blue-Violet | #6456B7 |
| 11 | Violet | #8359A3 |
| 12 | Red-Violet | #C0448F |
| 13 | Carnation Pink | #FFAACC |
| 14 | Apricot | #FDD9B5 |
| 15 | Peach | #FFCBA4 |
| 16 | Brown | #AF593E |
| 17 | Raw Sienna | #D68A59 |
| 18 | Tan | #FAA76C |
| 19 | Burnt Sienna | #EA7E5D |
| 20 | Sky Blue | #76D7EA |
| 21 | Gray | #8B8680 |
| 22 | Black | #000000 |
| 23 | White | #FFFFFF |
| 24 | Maize | #F2C649 |

## Method: edge-aware cell coloring

1. Sobel magnitude on a luminance copy, averaged per cell. Cells at or above the 80th percentile of strength (and at least 0.01) are edge cells.
2. Edge cells: split the cell's pixels at the block's mean luminance; a cell darker than its 3x3 neighbourhood takes the dominant crayon of its darker side, any other edge cell the dominant crayon of its lighter side (dominant = most common nearest crayon among that side's pixels).
3. Flat cells: mean of the block in Lab, snapped to the nearest crayon (CIE76 distance in Lab).
4. Smoothing: one pass recolors single-cell islands (no 4-neighbour of the same crayon) to their most common neighbour crayon, unless the cell is an edge cell.

Edge detector used: Sobel (scikit-image). Runtime covers resize + coloring, not rendering.

## Previews, originals and blank grids

Each comparison image shows the original (left) beside the colored preview (right). The blank grid shows numbers only.

### 01-astronaut

**24x32** - edge rule on 154 of 768 cells, 36 islands smoothed, 122 ms; recognizable (proxy)

![01-astronaut 24x32 original | preview](picture-method/edge-aware/01-astronaut/compare-24x32.png)
![01-astronaut 24x32 blank grid](picture-method/edge-aware/01-astronaut/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 39 islands smoothed, 124 ms; recognizable (proxy)

![01-astronaut 36x48 original | preview](picture-method/edge-aware/01-astronaut/compare-36x48.png)
![01-astronaut 36x48 blank grid](picture-method/edge-aware/01-astronaut/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 73 islands smoothed, 225 ms; recognizable (proxy)

![01-astronaut 48x64 original | preview](picture-method/edge-aware/01-astronaut/compare-48x64.png)
![01-astronaut 48x64 blank grid](picture-method/edge-aware/01-astronaut/blank-48x64.png)

### 02-chelsea-cat

**24x32** - edge rule on 154 of 768 cells, 17 islands smoothed, 40 ms; NOT recognizable (proxy): only 4 crayons used

![02-chelsea-cat 24x32 original | preview](picture-method/edge-aware/02-chelsea-cat/compare-24x32.png)
![02-chelsea-cat 24x32 blank grid](picture-method/edge-aware/02-chelsea-cat/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 33 islands smoothed, 102 ms; recognizable (proxy)

![02-chelsea-cat 36x48 original | preview](picture-method/edge-aware/02-chelsea-cat/compare-36x48.png)
![02-chelsea-cat 36x48 blank grid](picture-method/edge-aware/02-chelsea-cat/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 31 islands smoothed, 377 ms; recognizable (proxy)

![02-chelsea-cat 48x64 original | preview](picture-method/edge-aware/02-chelsea-cat/compare-48x64.png)
![02-chelsea-cat 48x64 blank grid](picture-method/edge-aware/02-chelsea-cat/blank-48x64.png)

### 03-coffee

**24x32** - edge rule on 154 of 768 cells, 25 islands smoothed, 52 ms; recognizable (proxy)

![03-coffee 24x32 original | preview](picture-method/edge-aware/03-coffee/compare-24x32.png)
![03-coffee 24x32 blank grid](picture-method/edge-aware/03-coffee/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 34 islands smoothed, 123 ms; recognizable (proxy)

![03-coffee 36x48 original | preview](picture-method/edge-aware/03-coffee/compare-36x48.png)
![03-coffee 36x48 blank grid](picture-method/edge-aware/03-coffee/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 37 islands smoothed, 715 ms; recognizable (proxy)

![03-coffee 48x64 original | preview](picture-method/edge-aware/03-coffee/compare-48x64.png)
![03-coffee 48x64 blank grid](picture-method/edge-aware/03-coffee/blank-48x64.png)

### 04-rocket

**24x32** - edge rule on 154 of 768 cells, 0 islands smoothed, 108 ms; NOT recognizable (proxy): light/dark structure differs from the original (luminance SSIM 0.32 < 0.45)

![04-rocket 24x32 original | preview](picture-method/edge-aware/04-rocket/compare-24x32.png)
![04-rocket 24x32 blank grid](picture-method/edge-aware/04-rocket/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 5 islands smoothed, 126 ms; NOT recognizable (proxy): light/dark structure differs from the original (luminance SSIM 0.30 < 0.45)

![04-rocket 36x48 original | preview](picture-method/edge-aware/04-rocket/compare-36x48.png)
![04-rocket 36x48 blank grid](picture-method/edge-aware/04-rocket/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 5 islands smoothed, 389 ms; NOT recognizable (proxy): light/dark structure differs from the original (luminance SSIM 0.29 < 0.45)

![04-rocket 48x64 original | preview](picture-method/edge-aware/04-rocket/compare-48x64.png)
![04-rocket 48x64 blank grid](picture-method/edge-aware/04-rocket/blank-48x64.png)

### 05-raccoon

**24x32** - edge rule on 154 of 768 cells, 6 islands smoothed, 58 ms; NOT recognizable (proxy): only 4 crayons used

![05-raccoon 24x32 original | preview](picture-method/edge-aware/05-raccoon/compare-24x32.png)
![05-raccoon 24x32 blank grid](picture-method/edge-aware/05-raccoon/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 17 islands smoothed, 104 ms; recognizable (proxy)

![05-raccoon 36x48 original | preview](picture-method/edge-aware/05-raccoon/compare-36x48.png)
![05-raccoon 36x48 blank grid](picture-method/edge-aware/05-raccoon/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 37 islands smoothed, 319 ms; recognizable (proxy)

![05-raccoon 48x64 original | preview](picture-method/edge-aware/05-raccoon/compare-48x64.png)
![05-raccoon 48x64 blank grid](picture-method/edge-aware/05-raccoon/blank-48x64.png)

### 06-mona-lisa

**24x32** - edge rule on 154 of 768 cells, 11 islands smoothed, 236 ms; recognizable (proxy)

![06-mona-lisa 24x32 original | preview](picture-method/edge-aware/06-mona-lisa/compare-24x32.png)
![06-mona-lisa 24x32 blank grid](picture-method/edge-aware/06-mona-lisa/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 16 islands smoothed, 759 ms; recognizable (proxy)

![06-mona-lisa 36x48 original | preview](picture-method/edge-aware/06-mona-lisa/compare-36x48.png)
![06-mona-lisa 36x48 blank grid](picture-method/edge-aware/06-mona-lisa/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 18 islands smoothed, 1954 ms; recognizable (proxy)

![06-mona-lisa 48x64 original | preview](picture-method/edge-aware/06-mona-lisa/compare-48x64.png)
![06-mona-lisa 48x64 blank grid](picture-method/edge-aware/06-mona-lisa/blank-48x64.png)

### 07-migrant-mother

**24x32** - edge rule on 154 of 768 cells, 4 islands smoothed, 302 ms; NOT recognizable (proxy): only 3 crayons used

![07-migrant-mother 24x32 original | preview](picture-method/edge-aware/07-migrant-mother/compare-24x32.png)
![07-migrant-mother 24x32 blank grid](picture-method/edge-aware/07-migrant-mother/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 10 islands smoothed, 419 ms; NOT recognizable (proxy): only 3 crayons used

![07-migrant-mother 36x48 original | preview](picture-method/edge-aware/07-migrant-mother/compare-36x48.png)
![07-migrant-mother 36x48 blank grid](picture-method/edge-aware/07-migrant-mother/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 7 islands smoothed, 582 ms; NOT recognizable (proxy): only 3 crayons used

![07-migrant-mother 48x64 original | preview](picture-method/edge-aware/07-migrant-mother/compare-48x64.png)
![07-migrant-mother 48x64 blank grid](picture-method/edge-aware/07-migrant-mother/blank-48x64.png)

### 08-lunch-atop-skyscraper

**24x32** - edge rule on 154 of 768 cells, 13 islands smoothed, 104 ms; NOT recognizable (proxy): light/dark structure differs from the original (luminance SSIM 0.45 < 0.45); only 3 crayons used

![08-lunch-atop-skyscraper 24x32 original | preview](picture-method/edge-aware/08-lunch-atop-skyscraper/compare-24x32.png)
![08-lunch-atop-skyscraper 24x32 blank grid](picture-method/edge-aware/08-lunch-atop-skyscraper/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 18 islands smoothed, 215 ms; NOT recognizable (proxy): only 3 crayons used

![08-lunch-atop-skyscraper 36x48 original | preview](picture-method/edge-aware/08-lunch-atop-skyscraper/compare-36x48.png)
![08-lunch-atop-skyscraper 36x48 blank grid](picture-method/edge-aware/08-lunch-atop-skyscraper/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 23 islands smoothed, 334 ms; NOT recognizable (proxy): only 3 crayons used

![08-lunch-atop-skyscraper 48x64 original | preview](picture-method/edge-aware/08-lunch-atop-skyscraper/compare-48x64.png)
![08-lunch-atop-skyscraper 48x64 blank grid](picture-method/edge-aware/08-lunch-atop-skyscraper/blank-48x64.png)

### 09-golden-retriever

**24x32** - edge rule on 154 of 768 cells, 11 islands smoothed, 96 ms; recognizable (proxy)

![09-golden-retriever 24x32 original | preview](picture-method/edge-aware/09-golden-retriever/compare-24x32.png)
![09-golden-retriever 24x32 blank grid](picture-method/edge-aware/09-golden-retriever/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 24 islands smoothed, 169 ms; recognizable (proxy)

![09-golden-retriever 36x48 original | preview](picture-method/edge-aware/09-golden-retriever/compare-36x48.png)
![09-golden-retriever 36x48 blank grid](picture-method/edge-aware/09-golden-retriever/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 47 islands smoothed, 394 ms; recognizable (proxy)

![09-golden-retriever 48x64 original | preview](picture-method/edge-aware/09-golden-retriever/compare-48x64.png)
![09-golden-retriever 48x64 blank grid](picture-method/edge-aware/09-golden-retriever/blank-48x64.png)

### 10-hopetoun-falls

**24x32** - edge rule on 154 of 768 cells, 1 islands smoothed, 101 ms; recognizable (proxy)

![10-hopetoun-falls 24x32 original | preview](picture-method/edge-aware/10-hopetoun-falls/compare-24x32.png)
![10-hopetoun-falls 24x32 blank grid](picture-method/edge-aware/10-hopetoun-falls/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 12 islands smoothed, 193 ms; recognizable (proxy)

![10-hopetoun-falls 36x48 original | preview](picture-method/edge-aware/10-hopetoun-falls/compare-36x48.png)
![10-hopetoun-falls 36x48 blank grid](picture-method/edge-aware/10-hopetoun-falls/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 14 islands smoothed, 390 ms; recognizable (proxy)

![10-hopetoun-falls 48x64 original | preview](picture-method/edge-aware/10-hopetoun-falls/compare-48x64.png)
![10-hopetoun-falls 48x64 blank grid](picture-method/edge-aware/10-hopetoun-falls/blank-48x64.png)

### 11-shibuya-crossing

**24x32** - edge rule on 154 of 768 cells, 36 islands smoothed, 97 ms; recognizable (proxy)

![11-shibuya-crossing 24x32 original | preview](picture-method/edge-aware/11-shibuya-crossing/compare-24x32.png)
![11-shibuya-crossing 24x32 blank grid](picture-method/edge-aware/11-shibuya-crossing/blank-24x32.png)

**36x48** - edge rule on 346 of 1728 cells, 61 islands smoothed, 273 ms; recognizable (proxy)

![11-shibuya-crossing 36x48 original | preview](picture-method/edge-aware/11-shibuya-crossing/compare-36x48.png)
![11-shibuya-crossing 36x48 blank grid](picture-method/edge-aware/11-shibuya-crossing/blank-36x48.png)

**48x64** - edge rule on 615 of 3072 cells, 96 islands smoothed, 441 ms; recognizable (proxy)

![11-shibuya-crossing 48x64 original | preview](picture-method/edge-aware/11-shibuya-crossing/compare-48x64.png)
![11-shibuya-crossing 48x64 blank grid](picture-method/edge-aware/11-shibuya-crossing/blank-48x64.png)

## Contact sheets

All images in pinned order, original | preview in each tile.

### 24x32

![contact sheet 24x32](picture-method/edge-aware/contact-sheet-24x32.png)

### 36x48

![contact sheet 36x48](picture-method/edge-aware/contact-sheet-36x48.png)

### 48x64

![contact sheet 48x64](picture-method/edge-aware/contact-sheet-48x64.png)


## Recognizability notes

These notes are an AUTOMATED PROXY, not a human viewing. A preview counts as recognizable when, against the original's per-cell mean, its luminance SSIM is >= 0.45, the correlation of Sobel edge maps is >= 0.45 and at least 5 crayons are used. Look at the contact sheets to confirm by eye.

### Per image and density

| image | density | recognizable | luma SSIM | edge corr | mean dE76 | why not |
|---|---|---|---|---|---|---|
| 01-astronaut | 24x32 | yes | 0.76 | 0.84 | 16.6 | - |
| 02-chelsea-cat | 24x32 | no | 0.69 | 0.67 | 20.6 | only 4 crayons used |
| 03-coffee | 24x32 | yes | 0.75 | 0.70 | 19.8 | - |
| 04-rocket | 24x32 | no | 0.32 | 0.63 | 28.9 | light/dark structure differs from the original (luminance SSIM 0.32 < 0.45) |
| 05-raccoon | 24x32 | no | 0.60 | 0.69 | 20.0 | only 4 crayons used |
| 06-mona-lisa | 24x32 | yes | 0.63 | 0.76 | 22.8 | - |
| 07-migrant-mother | 24x32 | no | 0.57 | 0.57 | 15.2 | only 3 crayons used |
| 08-lunch-atop-skyscraper | 24x32 | no | 0.45 | 0.63 | 20.6 | light/dark structure differs from the original (luminance SSIM 0.45 < 0.45); only 3 crayons used |
| 09-golden-retriever | 24x32 | yes | 0.66 | 0.52 | 19.2 | - |
| 10-hopetoun-falls | 24x32 | yes | 0.58 | 0.64 | 19.7 | - |
| 11-shibuya-crossing | 24x32 | yes | 0.58 | 0.58 | 20.0 | - |
| 01-astronaut | 36x48 | yes | 0.74 | 0.84 | 16.5 | - |
| 02-chelsea-cat | 36x48 | yes | 0.68 | 0.72 | 20.2 | - |
| 03-coffee | 36x48 | yes | 0.71 | 0.74 | 19.1 | - |
| 04-rocket | 36x48 | no | 0.30 | 0.63 | 28.5 | light/dark structure differs from the original (luminance SSIM 0.30 < 0.45) |
| 05-raccoon | 36x48 | yes | 0.55 | 0.66 | 19.9 | - |
| 06-mona-lisa | 36x48 | yes | 0.56 | 0.75 | 22.4 | - |
| 07-migrant-mother | 36x48 | no | 0.54 | 0.59 | 14.8 | only 3 crayons used |
| 08-lunch-atop-skyscraper | 36x48 | no | 0.48 | 0.67 | 19.7 | only 3 crayons used |
| 09-golden-retriever | 36x48 | yes | 0.57 | 0.47 | 19.3 | - |
| 10-hopetoun-falls | 36x48 | yes | 0.50 | 0.57 | 19.6 | - |
| 11-shibuya-crossing | 36x48 | yes | 0.61 | 0.65 | 20.1 | - |
| 01-astronaut | 48x64 | yes | 0.74 | 0.83 | 15.6 | - |
| 02-chelsea-cat | 48x64 | yes | 0.67 | 0.75 | 20.0 | - |
| 03-coffee | 48x64 | yes | 0.69 | 0.78 | 18.5 | - |
| 04-rocket | 48x64 | no | 0.29 | 0.59 | 28.6 | light/dark structure differs from the original (luminance SSIM 0.29 < 0.45) |
| 05-raccoon | 48x64 | yes | 0.52 | 0.66 | 19.8 | - |
| 06-mona-lisa | 48x64 | yes | 0.51 | 0.74 | 22.2 | - |
| 07-migrant-mother | 48x64 | no | 0.52 | 0.58 | 14.9 | only 3 crayons used |
| 08-lunch-atop-skyscraper | 48x64 | no | 0.50 | 0.67 | 19.2 | only 3 crayons used |
| 09-golden-retriever | 48x64 | yes | 0.52 | 0.46 | 19.4 | - |
| 10-hopetoun-falls | 48x64 | yes | 0.49 | 0.58 | 19.3 | - |
| 11-shibuya-crossing | 48x64 | yes | 0.61 | 0.61 | 20.6 | - |

### Roll-up by category (recognizable / total)

| category | 24x32 | 36x48 | 48x64 |
|---|---|---|---|
| portrait | 2/2 | 2/2 | 2/2 |
| group | 0/2 | 0/2 | 0/2 |
| pet or animal | 1/3 | 3/3 | 3/3 |
| outdoor | 1/2 | 1/2 | 1/2 |
| indoor | 1/1 | 1/1 | 1/1 |
| cluttered | 1/1 | 1/1 | 1/1 |

## Palette usage

| density | avg distinct crayons / picture | avg share of cells in top-3 crayons | crayons never used (all pictures) | which |
|---|---|---|---|---|
| 24x32 | 7.8 | 87.8% | 1 | Sky Blue |
| 36x48 | 8.3 | 87.3% | 1 | Red-Violet |
| 48x64 | 9.0 | 87.1% | 1 | Red-Violet |

## Blank-sheet privacy

- 24x32: OK - 11 blank grids: 576x768 px, cell 24 px, identical grid lines, grayscale only
- 36x48: OK - 11 blank grids: 576x768 px, cell 16 px, identical grid lines, grayscale only
- 48x64: OK - 11 blank grids: 576x768 px, cell 12 px, identical grid lines, grayscale only

Blank grids contain only numbers on white cells with uniform grey grid lines; no outlines, shading or colors.

Leakage = share of adjacent cell pairs (horizontal + vertical) carrying the same number. 'Chance' is the share expected if the same numbers were shuffled over the grid; the excess is the structure the layout gives away.

| density | adjacent same-number share (avg) | chance | excess |
|---|---|---|---|
| 24x32 | 75.1% | 36.8% | +38.3 pts |
| 36x48 | 77.7% | 36.1% | +41.6 pts |
| 48x64 | 79.1% | 35.9% | +43.3 pts |

Example blank sheets at 36x48:

**01-astronaut** (least leaky, 69.2% adjacent same-number)

![blank 01-astronaut](picture-method/edge-aware/01-astronaut/blank-36x48.png)

**06-mona-lisa** (median, 79.9% adjacent same-number)

![blank 06-mona-lisa](picture-method/edge-aware/06-mona-lisa/blank-36x48.png)

**04-rocket** (most leaky, 86.2% adjacent same-number)

![blank 04-rocket](picture-method/edge-aware/04-rocket/blank-36x48.png)

Can the subject be guessed from the numbers alone? NOT TESTED: this script has no human or model viewer. The excess over chance shows that regions of equal numbers are readable as shapes; a high excess means large same-number patches that outline the subject's major regions.

## Practicality for a child

Island = a cell with no 4-neighbour of the same crayon. Run length = average length of same-number runs along a row.

| density | avg islands / picture | islands as share of cells | avg run length (cells) |
|---|---|---|---|
| 24x32 | 16.5 | 2.14% | 3.69 |
| 36x48 | 35.8 | 2.07% | 4.17 |
| 48x64 | 63.0 | 2.05% | 4.58 |

### Per image

| image | density | islands | avg run length | cells using edge rule | islands smoothed |
|---|---|---|---|---|---|
| 01-astronaut | 24x32 | 17 | 2.59 | 154 (20%) | 36 |
| 02-chelsea-cat | 24x32 | 16 | 2.63 | 154 (20%) | 17 |
| 03-coffee | 24x32 | 32 | 2.84 | 154 (20%) | 25 |
| 04-rocket | 24x32 | 17 | 4.39 | 154 (20%) | 0 |
| 05-raccoon | 24x32 | 13 | 4.52 | 154 (20%) | 6 |
| 06-mona-lisa | 24x32 | 16 | 3.75 | 154 (20%) | 11 |
| 07-migrant-mother | 24x32 | 10 | 4.71 | 154 (20%) | 4 |
| 08-lunch-atop-skyscraper | 24x32 | 8 | 3.12 | 154 (20%) | 13 |
| 09-golden-retriever | 24x32 | 12 | 4.36 | 154 (20%) | 11 |
| 10-hopetoun-falls | 24x32 | 15 | 4.15 | 154 (20%) | 1 |
| 11-shibuya-crossing | 24x32 | 25 | 3.56 | 154 (20%) | 36 |
| 01-astronaut | 36x48 | 52 | 2.86 | 346 (20%) | 39 |
| 02-chelsea-cat | 36x48 | 27 | 3.13 | 346 (20%) | 33 |
| 03-coffee | 36x48 | 56 | 3.54 | 346 (20%) | 34 |
| 04-rocket | 36x48 | 31 | 5.20 | 346 (20%) | 5 |
| 05-raccoon | 36x48 | 22 | 5.16 | 346 (20%) | 17 |
| 06-mona-lisa | 36x48 | 35 | 4.62 | 346 (20%) | 16 |
| 07-migrant-mother | 36x48 | 17 | 5.65 | 346 (20%) | 10 |
| 08-lunch-atop-skyscraper | 36x48 | 20 | 3.38 | 346 (20%) | 18 |
| 09-golden-retriever | 36x48 | 40 | 4.41 | 346 (20%) | 24 |
| 10-hopetoun-falls | 36x48 | 37 | 4.44 | 346 (20%) | 12 |
| 11-shibuya-crossing | 36x48 | 57 | 3.49 | 346 (20%) | 61 |
| 01-astronaut | 48x64 | 90 | 3.27 | 615 (20%) | 73 |
| 02-chelsea-cat | 48x64 | 61 | 3.42 | 615 (20%) | 31 |
| 03-coffee | 48x64 | 89 | 4.07 | 615 (20%) | 37 |
| 04-rocket | 48x64 | 48 | 6.01 | 615 (20%) | 5 |
| 05-raccoon | 48x64 | 44 | 5.52 | 615 (20%) | 37 |
| 06-mona-lisa | 48x64 | 44 | 5.31 | 615 (20%) | 18 |
| 07-migrant-mother | 48x64 | 25 | 5.80 | 615 (20%) | 7 |
| 08-lunch-atop-skyscraper | 48x64 | 44 | 3.71 | 615 (20%) | 23 |
| 09-golden-retriever | 48x64 | 68 | 4.73 | 615 (20%) | 47 |
| 10-hopetoun-falls | 48x64 | 74 | 4.92 | 615 (20%) | 14 |
| 11-shibuya-crossing | 48x64 | 106 | 3.58 | 615 (20%) | 96 |

## Edge rule usage

| density | avg cells on edge rule | share of cells | avg islands smoothed |
|---|---|---|---|
| 24x32 | 154 | 20.1% | 14.5 |
| 36x48 | 346 | 20.0% | 24.5 |
| 48x64 | 615 | 20.0% | 35.3 |

## Runtime per image (seconds, resize + coloring)

| image | 24x32 | 36x48 | 48x64 |
|---|---|---|---|
| 01-astronaut | 0.12 | 0.12 | 0.22 |
| 02-chelsea-cat | 0.04 | 0.10 | 0.38 |
| 03-coffee | 0.05 | 0.12 | 0.72 |
| 04-rocket | 0.11 | 0.13 | 0.39 |
| 05-raccoon | 0.06 | 0.10 | 0.32 |
| 06-mona-lisa | 0.24 | 0.76 | 1.95 |
| 07-migrant-mother | 0.30 | 0.42 | 0.58 |
| 08-lunch-atop-skyscraper | 0.10 | 0.22 | 0.33 |
| 09-golden-retriever | 0.10 | 0.17 | 0.39 |
| 10-hopetoun-falls | 0.10 | 0.19 | 0.39 |
| 11-shibuya-crossing | 0.10 | 0.27 | 0.44 |

## Verdict

Rule: among densities with at most 3% island cells, pick the one with the most recognizable (proxy) pictures, then the highest luminance SSIM.
- 24x32: 6/11 recognizable, luminance SSIM 0.60, islands 2.14% of cells
- 36x48: 8/11 recognizable, luminance SSIM 0.57, islands 2.07% of cells
- 48x64: 8/11 recognizable, luminance SSIM 0.55, islands 2.05% of cells
- **Best density by this rule: 36x48.**
- Failure cases (proxy): 02-chelsea-cat @ 24x32, 04-rocket @ 24x32, 05-raccoon @ 24x32, 07-migrant-mother @ 24x32, 08-lunch-atop-skyscraper @ 24x32, 04-rocket @ 36x48, 07-migrant-mother @ 36x48, 08-lunch-atop-skyscraper @ 36x48, 04-rocket @ 48x64, 07-migrant-mother @ 48x64, 08-lunch-atop-skyscraper @ 48x64

