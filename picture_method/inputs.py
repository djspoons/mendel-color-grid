"""The 11 pinned input images: fetch them, save as photos/NN-name.jpg, hash them."""

import hashlib
import io
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageOps

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
COMMONS_FILEPATH = "https://commons.wikimedia.org/wiki/Special:FilePath/"
COMMONS_WIDTH = 1600
USER_AGENT = "picture-method-exploration/1.0 (research script; Pillow/urllib)"


@dataclass(frozen=True)
class PinnedImage:
    name: str  # e.g. "01-astronaut"
    category: str
    source_kind: str  # "bundled" or "commons"
    source_ref: str  # bundled call or Commons file title
    license_note: str = ""  # used for bundled images only


# The order here is the pinned order; do not add, drop, swap or reorder.
PINNED = [
    PinnedImage("01-astronaut", "portrait", "bundled", "skimage.data.astronaut()",
                "public domain (NASA photo), as documented by scikit-image"),
    PinnedImage("02-chelsea-cat", "pet or animal", "bundled", "skimage.data.chelsea()",
                "CC0, as documented by scikit-image"),
    PinnedImage("03-coffee", "indoor", "bundled", "skimage.data.coffee()",
                "CC0, as documented by scikit-image"),
    PinnedImage("04-rocket", "outdoor", "bundled", "skimage.data.rocket()",
                "public domain, as documented by scikit-image"),
    PinnedImage("05-raccoon", "pet or animal", "bundled", "scipy.datasets.face()",
                "public domain (public-domain-image.com), as documented by SciPy"),
    PinnedImage("06-mona-lisa", "portrait", "commons",
                "Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg"),
    PinnedImage("07-migrant-mother", "group", "commons", "Lange-MigrantMother02.jpg"),
    PinnedImage("08-lunch-atop-skyscraper", "group", "commons", "Lunch atop a Skyscraper.jpg"),
    PinnedImage("09-golden-retriever", "pet or animal", "commons", "Golden Retriever Dukedestiny01.jpg"),
    PinnedImage("10-hopetoun-falls", "outdoor", "commons", "Hopetoun falls.jpg"),
    PinnedImage("11-shibuya-crossing", "cluttered", "commons",
                "Tokyo Shibuya Scramble Crossing 2018-10-09.jpg"),
]


@dataclass
class LoadedImage:
    pinned: PinnedImage
    status: str = "OK"  # "OK" or "MISSING"
    reason: str = ""
    image: Image.Image = None
    path: str = ""
    size: tuple = (0, 0)
    sha256: str = ""
    source: str = ""
    license: str = ""
    notes: list = field(default_factory=list)

    @property
    def name(self):
        return self.pinned.name

    @property
    def ok(self):
        return self.status == "OK"


def _bundled_array(ref):
    if ref == "skimage.data.astronaut()":
        from skimage import data
        return data.astronaut()
    if ref == "skimage.data.chelsea()":
        from skimage import data
        return data.chelsea()
    if ref == "skimage.data.coffee()":
        from skimage import data
        return data.coffee()
    if ref == "skimage.data.rocket()":
        from skimage import data
        return data.rocket()
    if ref == "scipy.datasets.face()":
        import scipy.datasets
        return scipy.datasets.face()
    raise ValueError(f"unknown bundled source {ref}")


def _http_get(url, retries=4):
    """GET with a User-Agent and a short backoff on throttling or server errors."""
    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            retryable = error.code in (429, 500, 502, 503, 504)
            if not retryable or attempt == retries - 1:
                raise
        except urllib.error.URLError:
            if attempt == retries - 1:
                raise
        time.sleep(2 * 2**attempt)


def _commons_fetch(title):
    """Return (jpeg bytes, source url, license, notes) for an exact Commons file title.

    Route: the Commons API (imageinfo, 1600px-wide thumbnail when the original is
    wider), which also reports the license; Special:FilePath is the fallback.
    """
    query = urllib.parse.urlencode({
        "action": "query", "titles": "File:" + title, "prop": "imageinfo",
        "iiprop": "url|size|extmetadata", "iiurlwidth": COMMONS_WIDTH,
        "format": "json", "formatversion": 2,
    })
    try:
        page = json.loads(_http_get(COMMONS_API + "?" + query))["query"]["pages"][0]
        if page.get("missing"):
            raise LookupError(f"Commons has no file titled '{title}'")
        info = page["imageinfo"][0]
        license_name = info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "not reported")
        use_thumb = info["width"] > COMMONS_WIDTH
        url = info["thumburl"] if use_thumb else info["url"]
        notes = [f"original on Commons: {info['width']}x{info['height']} px; "
                 + (f"fetched the {COMMONS_WIDTH}px-wide thumbnail" if use_thumb else "fetched the original")]
        return _http_get(url), info["descriptionurl"], license_name, notes
    except LookupError:
        raise
    except Exception as error:  # API unreachable or odd answer: fall back to FilePath
        url = COMMONS_FILEPATH + urllib.parse.quote(title.replace(" ", "_")) + f"?width={COMMONS_WIDTH}"
        notes = [f"Commons API failed ({error!r}); used Special:FilePath, license not recorded"]
        return _http_get(url), url, "not recorded (Commons API failed)", notes


def load_image(pinned, photos_dir):
    """Fetch one pinned image, save it under photos/, and re-read it from that file."""
    loaded = LoadedImage(pinned)
    path = Path(photos_dir) / f"{pinned.name}.jpg"
    try:
        if pinned.source_kind == "bundled":
            buffer = io.BytesIO()
            Image.fromarray(_bundled_array(pinned.source_ref)).convert("RGB").save(
                buffer, "JPEG", quality=95)
            data = buffer.getvalue()
            loaded.source = pinned.source_ref
            loaded.license = pinned.license_note
            loaded.notes.append("bundled array re-encoded as JPEG quality 95")
        else:
            data, loaded.source, loaded.license, notes = _commons_fetch(pinned.source_ref)
            loaded.notes.extend(notes)
        path.write_bytes(data)
        with Image.open(path) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGB")
        loaded.image = image
        loaded.path = str(path)
        loaded.size = image.size
        loaded.sha256 = hashlib.sha256(data).hexdigest()
    except Exception as error:
        loaded.status = "MISSING"
        loaded.reason = f"{type(error).__name__}: {error}"
        loaded.source = pinned.source_ref
    return loaded


def load_all(photos_dir):
    Path(photos_dir).mkdir(parents=True, exist_ok=True)
    return [load_image(pinned, photos_dir) for pinned in PINNED]
