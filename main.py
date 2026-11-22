"""Copy the 21 November 2026 front page to the grader's output folder.

The picture itself is entry.png next to this file; this program only checks
that it is a whole 1024 by 1024 PNG inside the size cap, then writes it to
MAKEFUN_OUTPUT_DIR (or /output when that is unset). It fetches nothing,
draws nothing and needs nothing beyond the standard library.
"""
import struct
import sys
from hashlib import sha256
from os import environ
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"
SIZE_CAP = 1_048_576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_DIMS = (1024, 1024)


def load_picture():
    blob = PICTURE.read_bytes()
    if not blob.startswith(PNG_SIGNATURE):
        sys.exit("entry.png is not a PNG file")
    if len(blob) > SIZE_CAP:
        sys.exit(f"entry.png is {len(blob)} bytes, over the 1 MiB cap")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != EXPECTED_DIMS:
        sys.exit(f"entry.png is {width}x{height}, expected 1024x1024")
    return blob


def place_picture():
    blob = load_picture()
    out_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(blob)
    print(f"wrote {target} ({len(blob)} bytes, "
          f"sha256 {sha256(blob).hexdigest()})")


if __name__ == "__main__":
    place_picture()
