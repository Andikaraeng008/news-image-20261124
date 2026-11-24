"""The World Today -- Tuesday 24 November 2026.

Entry program for make.fun news-image-20261124. It writes the front
page to /output/entry.png.

The front page artwork is bundled with this repository as entry.png
(original work made for this edition: masthead "THE WORLD TODAY",
12 verified stories of Tuesday 24 November 2026, lead story on the
Seoul / Ulleung Island alert, three original illustrations). This
program copies it to the output path using the standard library only,
so it runs identically whether or not Pillow is installed, with no
network, and deterministically: both runs write the same bytes.
"""

import os
import shutil
import sys

try:
    from PIL import Image  # noqa: F401  (optional; never required)
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out = argv[1] if len(argv) > 1 else "/output/entry.png"
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, out)
    # The bundled file is the whole entry: PNG, 1024x1024, 514456 bytes.
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
