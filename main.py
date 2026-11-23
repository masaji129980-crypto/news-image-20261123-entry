#!/usr/bin/env python3
"""Entrypoint for the news-image-20261123 entry.

Renders the front page with draw.py and writes it as entry.png
into the output directory: $MAKEFUN_OUTPUT_DIR when set, else
/output (the grader's writable mount), else ./out for local runs.
The drawing is pure Pillow with fixed geometry, so two runs of
this program produce byte-identical output.
"""

import os
from pathlib import Path

import draw


def output_dir() -> Path:
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return Path(env)
    if Path("/output").is_dir():
        return Path("/output")
    return Path("out")


def main() -> None:
    target = output_dir()
    target.mkdir(parents=True, exist_ok=True)
    draw.build_image().save(target / "entry.png")
    print(f"wrote {target / 'entry.png'}")


if __name__ == "__main__":
    main()
