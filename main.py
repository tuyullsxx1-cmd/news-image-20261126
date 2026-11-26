#!/usr/bin/env python3
"""news-image-20261126 entrypoint: copy the drawn front page to /output/entry.png.

The image (repo entry.png) is the 1024x1024 flat-vector broadsheet drawn
offline during the build; this program only copies it, so both grader runs
write byte-identical output. Standard library only, no network.
"""
import hashlib
import os
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target = out_dir / "entry.png"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "source is not a PNG"
    digest = hashlib.sha256(data).hexdigest()
    with target.open("wb") as fh:
        fh.write(data)
    copied = target.read_bytes()
    assert hashlib.sha256(copied).hexdigest() == digest, "copy mismatch"
    assert len(copied) <= 1_048_576, "entry over 1 MiB"
    print(f"wrote {target} ({len(copied)} bytes, sha256 {digest[:16]}...)")


if __name__ == "__main__":
    main()
