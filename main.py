#!/usr/bin/env python3
"""Deliver the committed front-page image to the output directory.

The picture itself is drawn ahead of time by draw.py, which is a
build-time tool and is not needed here. At run time this entrypoint
only has one job: place the finished entry.png where the harness
expects it. It relies on the standard library alone, so it works in
any plain Python environment.

Output location: $MAKEFUN_OUTPUT_DIR when that variable is set,
otherwise /output. The directory is created when missing.
"""

import os
import shutil
from pathlib import Path


def output_directory() -> Path:
    from_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if from_env:
        return Path(from_env)
    return Path("/output")


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target_dir = output_directory()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    shutil.copyfile(source, target)
    print(f"copied {source} -> {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
