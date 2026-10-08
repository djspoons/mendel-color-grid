"""Shared constants: palette, densities, pinned images and output paths."""

from dataclasses import dataclass
from pathlib import Path

METHOD = "edge-aware"

ROOT = Path(".")
PHOTOS_DIR = ROOT / "photos"
DOCS_DIR = ROOT / "docs"
OUT_DIR = DOCS_DIR / "picture-method" / METHOD
REPORT_PATH = DOCS_DIR / "picture-method-results.md"

# Classic Crayola 24-count box. Cell numbers are the 1-based index in this list.
PALETTE = [
    ("Red", "ED0A3F"),
    ("Red-Orange", "FF681F"),
    ("Orange", "FF8833"),
    ("Yellow-Orange", "FFAE42"),
    ("Yellow", "FBE870"),
    ("Yellow-Green", "C5E17A"),
    ("Green", "01A638"),
    ("Blue-Green", "0D98BA"),
    ("Blue", "0066FF"),
    ("Blue-Violet", "6456B7"),
    ("Violet", "8359A3"),
    ("Red-Violet", "C0448F"),
    ("Carnation Pink", "FFAACC"),
    ("Apricot", "FDD9B5"),
    ("Peach", "FFCBA4"),
    ("Brown", "AF593E"),
    ("Raw Sienna", "D68A59"),
    ("Tan", "FAA76C"),
    ("Burnt Sienna", "EA7E5D"),
    ("Sky Blue", "76D7EA"),
    ("Gray", "8B8680"),
    ("Black", "000000"),
    ("White", "FFFFFF"),
    ("Maize", "F2C649"),
]

# (columns, rows), exactly three.
DENSITIES = [(24, 32), (36, 48), (48, 64)]

# Output preview size is the same for every density: cell_px * cols == 576.
PREVIEW_WIDTH = 576
PREVIEW_HEIGHT = 768

# Each grid cell is analysed from a SUPERSAMPLE x SUPERSAMPLE pixel block.
SUPERSAMPLE = 8

COMMONS_FILEPATH = "https://commons.wikimedia.org/wiki/Special:FilePath/{title}?width=1600"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "picture-method-exploration/0.1 (crayon-grid research script)"


@dataclass(frozen=True)
class ImageSpec:
    number: int
    name: str
    category: str
    bundled: str = ""        # name of the bundled loader, if any
    commons_title: str = ""  # exact Commons file title, if any

    @property
    def stem(self):
        return f"{self.number:02d}-{self.name}"

    @property
    def filename(self):
        return f"{self.stem}.jpg"


IMAGES = [
    ImageSpec(1, "astronaut", "portrait", bundled="skimage.data.astronaut()"),
    ImageSpec(2, "chelsea-cat", "pet or animal", bundled="skimage.data.chelsea()"),
    ImageSpec(3, "coffee", "indoor", bundled="skimage.data.coffee()"),
    ImageSpec(4, "rocket", "outdoor", bundled="skimage.data.rocket()"),
    ImageSpec(5, "raccoon", "pet or animal", bundled="scipy.datasets.face()"),
    ImageSpec(6, "mona-lisa", "portrait",
              commons_title="Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg"),
    ImageSpec(7, "migrant-mother", "group",
              commons_title="Lange-MigrantMother02.jpg"),
    ImageSpec(8, "lunch-atop-skyscraper", "group",
              commons_title="Lunch atop a Skyscraper.jpg"),
    ImageSpec(9, "golden-retriever", "pet or animal",
              commons_title="Golden Retriever Dukedestiny01.jpg"),
    ImageSpec(10, "hopetoun-falls", "outdoor",
              commons_title="Hopetoun falls.jpg"),
    ImageSpec(11, "shibuya-crossing", "cluttered",
              commons_title="Tokyo Shibuya Scramble Crossing 2018-10-09.jpg"),
]

CATEGORY_ORDER = ["portrait", "group", "pet or animal", "outdoor", "indoor", "cluttered"]
