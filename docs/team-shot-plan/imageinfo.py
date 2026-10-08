"""Standard-library JPEG/PNG header inspection and JPEG metadata stripping.

Reads only what the validator and fetch script need: format, pixel size and
which metadata blocks (EXIF, XMP, IPTC, PNG text chunks) are present.
"""
import struct

JPEG_SOI = b"\xff\xd8"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_SOF_MARKERS = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
_PNG_METADATA_CHUNKS = {b"eXIf": "EXIF", b"tEXt": "PNG text", b"zTXt": "PNG text", b"iTXt": "PNG text/XMP"}


class ImageError(ValueError):
    """The bytes are not a readable JPEG or PNG."""


class ImageInfo:
    def __init__(self, fmt, width, height, metadata):
        self.format = fmt
        self.width = width
        self.height = height
        self.metadata = metadata

    @property
    def long_edge(self):
        return max(self.width, self.height)

    @property
    def short_edge(self):
        return min(self.width, self.height)

    def __repr__(self):
        return "ImageInfo(%s %dx%d metadata=%s)" % (self.format, self.width, self.height, self.metadata)


def _jpeg_segments(data):
    """Yield (marker, start, end) for each segment; start..end spans the whole segment."""
    if data[:2] != JPEG_SOI:
        raise ImageError("not a JPEG (missing SOI)")
    pos = 2
    size = len(data)
    while pos < size:
        if data[pos] != 0xFF:
            raise ImageError("corrupt JPEG: expected marker at byte %d" % pos)
        while pos < size and data[pos] == 0xFF:
            pos += 1
        if pos >= size:
            break
        marker = data[pos]
        pos += 1
        if marker == 0xD9:
            return
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            continue
        if pos + 2 > size:
            raise ImageError("corrupt JPEG: truncated segment header")
        length = struct.unpack(">H", data[pos:pos + 2])[0]
        if length < 2 or pos + length > size:
            raise ImageError("corrupt JPEG: bad segment length")
        yield marker, pos - 2, pos + length
        if marker == 0xDA:  # start of scan: entropy-coded data follows
            return
        pos += length


def _jpeg_metadata_label(marker, payload):
    if marker == 0xE1 and payload.startswith(b"Exif\x00"):
        return "EXIF"
    if marker == 0xE1 and payload.startswith(b"http://ns.adobe.com/xap/"):
        return "XMP"
    if marker == 0xED:
        return "IPTC/Photoshop"
    if marker == 0xFE:
        return "JPEG comment"
    return None


def inspect_bytes(data):
    if data[:2] == JPEG_SOI:
        return _inspect_jpeg(data)
    if data[:8] == PNG_SIGNATURE:
        return _inspect_png(data)
    raise ImageError("unsupported or unrecognised image format")


def inspect_file(path):
    with open(path, "rb") as handle:
        return inspect_bytes(handle.read())


def _inspect_jpeg(data):
    width = height = None
    metadata = []
    for marker, start, end in _jpeg_segments(data):
        payload = data[start + 4:end]
        label = _jpeg_metadata_label(marker, payload)
        if label and label not in metadata:
            metadata.append(label)
        if marker in _SOF_MARKERS and width is None:
            if len(payload) < 5:
                raise ImageError("corrupt JPEG: short SOF segment")
            height, width = struct.unpack(">HH", payload[1:5])
    if not width or not height:
        raise ImageError("JPEG has no frame header with a size")
    return ImageInfo("jpeg", width, height, metadata)


def _inspect_png(data):
    pos = 8
    width = height = None
    metadata = []
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            if len(body) < 8:
                raise ImageError("corrupt PNG: short IHDR")
            width, height = struct.unpack(">II", body[:8])
        label = _PNG_METADATA_CHUNKS.get(ctype)
        if label and label not in metadata:
            metadata.append(label)
        if ctype == b"IEND":
            break
        pos += 12 + length
    if not width or not height:
        raise ImageError("PNG has no IHDR with a size")
    return ImageInfo("png", width, height, metadata)


def strip_jpeg_metadata(data):
    """Return the JPEG with EXIF, XMP, IPTC and comment segments removed (lossless)."""
    if data[:2] != JPEG_SOI:
        raise ImageError("not a JPEG (missing SOI)")
    out = bytearray(JPEG_SOI)
    last_end = 2
    for marker, start, end in _jpeg_segments(data):
        label = _jpeg_metadata_label(marker, data[start + 4:end])
        if label:
            out += data[last_end:start]
            last_end = end
    out += data[last_end:]
    return bytes(out)
