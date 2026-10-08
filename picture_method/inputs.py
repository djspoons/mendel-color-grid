"""Fetch the 11 pinned images, record provenance, and pre-process them."""

import hashlib
import io
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Optional

import requests
from PIL import Image

from . import config

CROP_RATIO = 3 / 4  # width / height


@dataclass
class LoadedImage:
    spec: config.ImageSpec
    path: Optional[object] = None
    image: Optional[Image.Image] = None
    source: str = ""
    license: str = ""
    sha256: str = ""
    size: tuple = (0, 0)
    note: str = ""
    missing_reason: str = ""
    crop_note: str = ""

    @property
    def missing(self):
        return self.image is None


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def center_crop_3x4(image):
    """Center-crop to 3:4 portrait. Returns (cropped image, human note)."""
    w, h = image.size
    target_w = min(w, round(h * CROP_RATIO))
    target_h = min(h, round(w / CROP_RATIO))
    if w / h > CROP_RATIO:
        left = (w - target_w) // 2
        box = (left, 0, left + target_w, h)
        note = f"{'landscape' if w > h else 'square-ish'} source: crop removes the sides ({w - target_w} px)"
    elif w / h < CROP_RATIO:
        top = (h - target_h) // 2
        box = (0, top, w, top + target_h)
        note = f"taller than 3:4: crop removes top and bottom ({h - target_h} px)"
    else:
        box = (0, 0, w, h)
        note = "already 3:4: no crop"
    return image.crop(box), note


def resize_to_grid(cropped, cols, rows):
    """Resize the 3:4 crop to cols*SUPERSAMPLE x rows*SUPERSAMPLE pixels."""
    s = config.SUPERSAMPLE
    return cropped.resize((cols * s, rows * s), Image.LANCZOS)


def _bundled_array(spec):
    if spec.bundled.startswith("skimage.data."):
        from skimage import data
        return getattr(data, spec.bundled.split(".")[-1].rstrip("()"))()
    if spec.bundled.startswith("scipy.datasets"):
        import scipy.datasets
        return scipy.datasets.face()
    raise ValueError(spec.bundled)


def _get_with_retry(url, params=None, attempts=4):
    last = None
    for attempt in range(attempts):
        try:
            resp = requests.get(url, params=params, timeout=60,
                                headers={"User-Agent": config.USER_AGENT})
            if resp.status_code == 200:
                return resp
            last = f"HTTP {resp.status_code}"
        except requests.RequestException as exc:
            last = f"{type(exc).__name__}: {exc}"
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(last)


def commons_license(title):
    """Best-effort license string from the Commons API."""
    try:
        resp = _get_with_retry(config.COMMONS_API, params={
            "action": "query", "titles": "File:" + title, "prop": "imageinfo",
            "iiprop": "extmetadata", "format": "json"}, attempts=2)
        page = next(iter(resp.json()["query"]["pages"].values()))
        meta = page["imageinfo"][0]["extmetadata"]
        return meta.get("LicenseShortName", {}).get("value", "unknown (not in metadata)")
    except Exception as exc:  # license lookup must not stop the run
        return f"unknown (Commons API lookup failed: {exc})"


def load_bundled(spec):
    loaded = LoadedImage(spec)
    array = _bundled_array(spec)
    image = Image.fromarray(array).convert("RGB")
    path = config.PHOTOS_DIR / spec.filename
    image.save(path, format="JPEG", quality=95)
    loaded.path = path
    loaded.image = Image.open(path).convert("RGB")
    loaded.source = spec.bundled
    loaded.license = "bundled with library (scikit-image / SciPy data; see library docs)"
    loaded.note = "re-encoded as JPEG q95"
    return loaded


def load_commons(spec):
    loaded = LoadedImage(spec)
    path = config.PHOTOS_DIR / spec.filename
    title = spec.commons_title
    url = config.COMMONS_FILEPATH.format(
        title=urllib.parse.quote(title.replace(" ", "_"), safe=""))
    loaded.source = f"Wikimedia Commons File:{title} (Special:FilePath, width=1600)"
    # Always fetch fresh so the run reads exactly the pinned title, never a stale file.
    try:
        data = _get_with_retry(url).content
        Image.open(io.BytesIO(data)).verify()
        path.write_bytes(data)
    except Exception as exc:
        loaded.missing_reason = f"could not fetch {url}: {exc}"
        return loaded
    loaded.path = path
    loaded.license = commons_license(title)
    loaded.image = Image.open(path).convert("RGB")
    return loaded


def load_all():
    config.PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    result = []
    for spec in config.IMAGES:
        try:
            loaded = load_bundled(spec) if spec.bundled else load_commons(spec)
        except Exception as exc:
            loaded = LoadedImage(spec, source=spec.bundled or spec.commons_title,
                                 missing_reason=f"{type(exc).__name__}: {exc}")
        if loaded.image is not None:
            loaded.sha256 = sha256_of(loaded.path)
            loaded.size = loaded.image.size
            _, loaded.crop_note = center_crop_3x4(loaded.image)
        result.append(loaded)
    return result
