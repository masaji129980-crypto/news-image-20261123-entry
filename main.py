# A working news-image-daily entry (Python 3.13, standard library only):
# its image is the entry.png beside this file, drawn in code by draw.py,
# and the program copies it to /output/entry.png. The gate takes a whole
# PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees
# exactly the bytes copied.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
