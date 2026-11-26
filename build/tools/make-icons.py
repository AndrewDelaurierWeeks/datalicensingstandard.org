"""The site's icons: the face of the cover's engraved device, cut from the sealed PDF.

Writes build/assets/icons/favicon-16.png, favicon-32.png, favicon-48.png, favicon.ico and
build/assets/apple-touch-icon.png (180 x 180). Run once after a change:
    python3 build/tools/make-icons.py --venue PATH_TO_VENUE
Needs PyMuPDF and Pillow. The engraving is under Part 7's license (Creative Commons Attribution 4.0
International). This script is under the MIT License (build/LICENSE).
"""
import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageFilter, ImageOps

FACE = (950, 800, 2200, 2050)       # the face, brow to chin, in the cover image's own pixels (3165 x 2192)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", required=True, type=Path)
    a = ap.parse_args()
    assets = Path(__file__).resolve().parent.parent / "assets"
    doc = fitz.open(a.venue / "TDLS-AI-v0.1.pdf")
    xref = doc[0].get_images(full=True)[0][0]                       # the cover's one image: the engraved device
    pix = fitz.Pixmap(doc, xref)
    if (pix.width, pix.height) != (3165, 2192): raise SystemExit(f"unexpected cover image size {pix.width} x {pix.height}")
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L").crop(FACE)
    im = im.filter(ImageFilter.GaussianBlur(1.4))                     # no moiré from the hatching when it is made small
    im = ImageOps.autocontrast(im, cutoff=1).point(lambda v: int(255 * (v / 255) ** 1.35))   # the features hold at 16 pixels
    master = im.resize((512, 512), Image.LANCZOS).convert("RGB")
    (assets / "icons").mkdir(exist_ok=True)
    for s in (16, 32, 48):
        master.resize((s, s), Image.LANCZOS).save(assets / "icons" / f"favicon-{s}.png", optimize=True)
    master.save(assets / "icons" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    master.resize((180, 180), Image.LANCZOS).save(assets / "apple-touch-icon.png", optimize=True)
    print("icons written to", assets)

if __name__ == "__main__":
    main()
