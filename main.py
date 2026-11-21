#!/usr/bin/env python3
"""news-image-20261121 entrypoint.

Copies the pre-built front page (entry.png) to the output directory and
verifies its integrity against the sha256 recorded at build time.
Standard library only; no network.
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "87b5143894bb54ce0844983ac33689d3194904fee84924d7935dad229688b42e"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.png integrity check failed: " + digest)
    if len(data) > 1048576:
        raise SystemExit("entry.png over the 1 MiB limit: " + str(len(data)))
    with open(target, "wb") as fh:
        fh.write(data)
    print("wrote " + target + " (" + str(len(data)) + " bytes, sha256 " + digest + ")")


if __name__ == "__main__":
    main()
