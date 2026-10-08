"""The 11 pinned images: fetching, hashing, and the shared 3:4 center-crop."""

import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

import numpy as np
from PIL import Image

USER_AGENT = "picture-method-exploration/1.0 (research script; Python urllib)"
COMMONS_WIDTH = 1600
BUNDLED_NOTE = "bundled sample; licence per the library's data docs (not verified at run time)"


@dataclass(frozen=True)
class ImageSpec:
    number: int
    name: str
    category: str
    kind: str  # "skimage", "scipy" or "commons"
    ref: str  # skimage function name, or Commons file title

    @property
    def filename(self):
        return f"{self.number:02d}-{self.name}.jpg"


PINNED = [
    ImageSpec(1, "astronaut", "portrait", "skimage", "astronaut"),
    ImageSpec(2, "chelsea-cat", "pet or animal", "skimage", "chelsea"),
    ImageSpec(3, "coffee", "indoor", "skimage", "coffee"),
    ImageSpec(4, "rocket", "outdoor", "skimage", "rocket"),
    ImageSpec(5, "raccoon", "pet or animal", "scipy", "face"),
    ImageSpec(6, "mona-lisa", "portrait", "commons", "Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg"),
    ImageSpec(7, "migrant-mother", "group", "commons", "Lange-MigrantMother02.jpg"),
    ImageSpec(8, "lunch-atop-skyscraper", "group", "commons", "Lunch atop a Skyscraper.jpg"),
    ImageSpec(9, "golden-retriever", "pet or animal", "commons", "Golden Retriever Dukedestiny01.jpg"),
    ImageSpec(10, "hopetoun-falls", "outdoor", "commons", "Hopetoun falls.jpg"),
    ImageSpec(11, "shibuya-crossing", "cluttered", "commons", "Tokyo Shibuya Scramble Crossing 2018-10-09.jpg"),
]


@dataclass
class SourceImage:
    spec: ImageSpec
    path: str
    status: str = "OK"  # "OK" or "MISSING"
    reason: str = ""
    source: str = ""
    license: str = ""
    width: int = 0
    height: int = 0
    original_size: str = ""
    sha256: str = ""
    pixel_sha256: str = ""
    crop_note: str = ""


def _http_get(url, retries=3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as exc:  # retry briefly, then report as MISSING
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{type(last).__name__}: {last}")


def _commons_metadata(title):
    query = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": "File:" + title,
            "prop": "imageinfo",
            "iiprop": "extmetadata|size",
            "format": "json",
        }
    )
    try:
        data = json.loads(_http_get("https://commons.wikimedia.org/w/api.php?" + query))
        info = next(iter(data["query"]["pages"].values()))["imageinfo"][0]
        meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "unknown")
        return license_name, f"{info['width']}x{info['height']}"
    except Exception as exc:
        return f"unknown (Commons metadata fetch failed: {exc})", ""


def _fetch_bundled(spec):
    if spec.kind == "skimage":
        from skimage import data

        arr = getattr(data, spec.ref)()
        source = f"skimage.data.{spec.ref}()"
    else:
        import scipy.datasets

        arr = scipy.datasets.face()
        source = "scipy.datasets.face()"
    arr = np.ascontiguousarray(arr[..., :3], dtype=np.uint8)
    return arr, source


def fetch_image(spec, photo_dir):
    """Fetch one pinned image into photo_dir; never substitutes another image."""
    os.makedirs(photo_dir, exist_ok=True)
    path = os.path.join(photo_dir, spec.filename)
    item = SourceImage(spec=spec, path=path)
    try:
        if spec.kind == "commons":
            url = (
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                + urllib.parse.quote(spec.ref.replace(" ", "_"))
                + f"?width={COMMONS_WIDTH}"
            )
            raw = _http_get(url)
            with open(path, "wb") as fh:
                fh.write(raw)
            img = Image.open(path)
            img.load()
            item.source = f"Wikimedia Commons File:{spec.ref} (Special:FilePath, width={COMMONS_WIDTH})"
            item.license, item.original_size = _commons_metadata(spec.ref)
            item.pixel_sha256 = hashlib.sha256(np.asarray(img.convert("RGB")).tobytes()).hexdigest()
        else:
            arr, item.source = _fetch_bundled(spec)
            Image.fromarray(arr).save(path, format="JPEG", quality=95)
            item.license = BUNDLED_NOTE
            item.original_size = f"{arr.shape[1]}x{arr.shape[0]}"
            item.pixel_sha256 = hashlib.sha256(arr.tobytes()).hexdigest()
        with open(path, "rb") as fh:
            item.sha256 = hashlib.sha256(fh.read()).hexdigest()
        with Image.open(path) as img:
            item.width, item.height = img.size
        item.crop_note = crop_note(item.width, item.height)
    except Exception as exc:
        item.status = "MISSING"
        item.reason = f"{type(exc).__name__}: {exc}"
        if os.path.exists(path):
            os.remove(path)
    return item


def fetch_all(photo_dir):
    return [fetch_image(spec, photo_dir) for spec in PINNED]


def crop_note(width, height):
    ratio = width / height
    if abs(ratio - 0.75) < 1e-3:
        return "already 3:4, nothing cropped"
    if ratio > 0.75:
        kept = height * 0.75 / width
        return f"landscape/wide source: crop removes the sides ({(1 - kept) * 100:.0f}% of the width)"
    kept = width / 0.75 / height
    return f"taller than 3:4: crop removes top and bottom ({(1 - kept) * 100:.0f}% of the height)"


def center_crop_3x4(img):
    """Center-crop to 3:4 portrait (width:height)."""
    w, h = img.size
    if w * 4 > h * 3:  # too wide: cut the sides
        new_w = (h * 3) // 4
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    new_h = (w * 4) // 3
    top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def load_cropped(item):
    with Image.open(item.path) as img:
        return center_crop_3x4(img.convert("RGB"))
