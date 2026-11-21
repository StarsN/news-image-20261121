"""Place the 21 November 2026 front page where the grader expects it.

The picture itself lives beside this file as entry.png; this program only
confirms it is a whole 1024 by 1024 PNG inside the size cap and copies it
into MAKEFUN_OUTPUT_DIR (or /output when that is unset). It fetches
nothing, generates nothing and needs nothing beyond the standard library.
"""
import struct
import sys
from hashlib import sha256
from os import environ
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"
CAP = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
WANT_SIZE = (1024, 1024)


def read_picture():
    blob = PICTURE.read_bytes()
    if not blob.startswith(PNG_MAGIC):
        sys.exit("entry.png is not a PNG file")
    if len(blob) > CAP:
        sys.exit(f"entry.png is {len(blob)} bytes, over the 1 MiB cap")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != WANT_SIZE:
        sys.exit(f"entry.png is {width}x{height}, expected 1024x1024")
    return blob


def place_front_page():
    blob = read_picture()
    out_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(blob)
    print(f"wrote {target} ({len(blob)} bytes, "
          f"sha256 {sha256(blob).hexdigest()})")


if __name__ == "__main__": place_front_page()
