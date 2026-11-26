"""The figures of page 4 of the sealed PDF, "The security elements, and what each one does", for its web page.

Writes build/assets/security/: the page's own images (the device, the face, the microprint, the thread, the square
mark, the band), taken from the PDF at their stored pixels and made smaller for the web; the four step icons, drawn
from the page at eight times its size; and the page's AI ML EVAL border, drawn from the page at 12 pixels to the
millimetre and cut into the nine pieces of a CSS border image (microprint-frame.png).
Run once after a change:
    python3 build/tools/make-security.py --venue PATH_TO_VENUE
Needs PyMuPDF and Pillow. This script is under the MIT License (build/LICENSE).
"""
import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageOps

MM = 72 / 25.4      # points to the millimetre

# each figure by its place on page 4 (points), and the width it is stored at for the web (twice its widest showing)
FIGURES = {"device": ((63, 216, 177, 282), 560), "face": ((184, 216, 266, 283), 400), "microprint": ((324, 216, 504, 282), 760),
           "thread": ((511, 216, 522, 282), 60), "mark": ((63, 528, 130, 595), 330), "band": ((136, 528, 272, 595), 560)}
ICONS = {"look": (66, 172, 116, 200), "magnify": (327, 172, 377, 208), "compare": (62, 474, 120, 512), "verify": (327, 484, 377, 512)}

# the border, in millimetres from the page's top left: a 10 mm band inside the 0.4 mm outer rule (its inner edge at 1.9)
# and outside the 0.2 mm inner rule (its outer edge at 11.9, 204.1 and 267.1). Each row holds whole words set from 3.385
# to 212.615, every row starting one word on from the row above; down the sides, three words at each edge. The tool cuts
# the border into the nine pieces of a CSS border image, each cut in the middle of a gap that every row shares: across,
# after the bands' first three words (they end by 10.776, the next start at 11.885) and their next three (19.345, 20.385),
# and before the right side's words (the bands' end by 204.115, the side's start at 205.224); down, between the top band
# and the sides (10.978, 11.922) and between the sides and the bottom band (267.075, 268.022). Three rows make one repeat
# down the sides, 1.707333 mm apart. The site sets the frame 10 mm wide (site.css) and the browser repeats each band and
# side piece a whole number of times. The outer cuts stop 0.01 mm short of the outer rule. A band piece repeated a whole
# number of times cannot meet both of the page's corners in step, so the right corners take each row's first three
# words (from 2.8305 to 11.3305), set where the right side's words sit: every row then runs on one word at a time and
# no word comes twice, as on the page.
R = 1.707333
XS = (1.91, (10.776 + 11.885) / 2, (19.345 + 20.385) / 2, (204.115 + 205.224) / 2, 214.09)    # the cuts across
YS = (1.91, (10.978 + 11.922) / 2, (10.978 + 11.922) / 2 + 3 * R, (267.075 + 268.022) / 2, 277.09)
PX = ((113, 102, 113), (114, 61, 114))      # each piece's size in pixels, about 12 to the millimetre: slice 114 113
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", required=True, type=Path)
    a = ap.parse_args()
    out = Path(__file__).resolve().parent.parent / "assets" / "security"
    out.mkdir(exist_ok=True)
    doc = fitz.open(a.venue / "TDLS-AI-v0.1.pdf"); p = doc[3]
    infos = p.get_image_info(xrefs=True)
    for name, (box, width) in FIGURES.items():
        hit = [i for i in infos if all(abs(u - v) < 1.5 for u, v in zip(i["bbox"], box))]
        if len(hit) != 1: raise SystemExit(f"page 4: no single image at {box} for {name}")
        pix = fitz.Pixmap(doc, hit[0]["xref"])
        if pix.n - pix.alpha != 3: pix = fitz.Pixmap(fitz.csRGB, pix)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        if name in ("mark", "thread"): im.save(out / f"{name}.png", optimize=True)
        else: im.save(out / f"{name}.webp", quality=88, method=6)     # the engravings: WebP, a third of the PNG's size
    for name, box in ICONS.items():
        pix = p.get_pixmap(matrix=fitz.Matrix(8, 8), clip=fitz.Rect(box), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.crop(ImageOps.invert(im.convert("L")).point(lambda v: 255 if v > 24 else 0).getbbox()).save(out / f"icon-{name}.png", optimize=True)   # cut to the icon
    frame = Image.new("L", (sum(PX[0]), sum(PX[1])), 255)
    xs, ys = (XS[0], XS[1], XS[3]), (YS[0], YS[1], YS[3])      # the left, middle and right pieces start here
    xe, ye = (XS[1], XS[2], XS[4]), (YS[1], YS[2], YS[4])
    for c in range(3):
        for r in range(3):
            if (c, r) == (1, 1): continue                          # the middle, which a border image leaves out
            x0, x1, y0, y1, w, h = xs[c], xe[c], ys[r], ye[r], PX[0][c], PX[1][r]
            if c == 2 and r != 1: x0, x1, w = XS[1] - 8.5, XS[1], round(8.5 * w / (XS[4] - XS[3]))     # a right corner
            sx, sy = w / ((x1 - x0) * MM), h / ((y1 - y0) * MM)
            pix = p.get_pixmap(matrix=fitz.Matrix(sx, 0, 0, sy, -x0 * MM * sx, -y0 * MM * sy), clip=fitz.Rect(x0 * MM, y0 * MM, x1 * MM, y1 * MM), alpha=False)
            if (pix.width, pix.height) != (w, h): raise SystemExit(f"border piece {c},{r}: {pix.width} x {pix.height}, expected {w} x {h}")
            im = Image.frombytes("RGB", (w, h), pix.samples).convert("L")
            if any(im.crop(e).getextrema()[0] < 250 for e in ((0, 0, 1, h), (w - 1, 0, w, h), (0, 0, w, 1), (0, h - 1, w, h))):
                raise SystemExit(f"border piece {c},{r}: its edge crosses a letter or a rule")
            frame.paste(im, (sum(PX[0][:c]), sum(PX[1][:r])))
    frame.save(out / "microprint-frame.png", optimize=True)
    print("page 4 figures written to", out)

if __name__ == "__main__":
    main()
