#!/usr/bin/env python3
"""
prep_photo.py — one-time local image prep.
Removes the background (rembg) and boosts local contrast (CLAHE) so the
subject sits on blank space with real highlights/shadows instead of a dark
blob. This matters most for face photos; for flat-art/logo sources it mostly
just cleans edges and evens out contrast.

Usage:
    python scripts/prep_photo.py path/to/source.jpg source-prepped.png
"""
import sys
import numpy as np
import cv2
from rembg import remove
from PIL import Image

# ---- tunables -------------------------------------------------------------
CLIP_LIMIT = 2.5      # CLAHE contrast strength
TILE_GRID = (8, 8)    # CLAHE tile grid size
OUTPUT_SIZE = 900      # long-edge resize before ASCII conversion
# ----------------------------------------------------------------------------


def prep(src_path: str, dst_path: str) -> None:
    with open(src_path, "rb") as f:
        input_bytes = f.read()

    # 1. remove background -> RGBA
    out_bytes = remove(input_bytes)
    rgba = Image.open(__import__("io").BytesIO(out_bytes)).convert("RGBA")

    # 2. resize (long edge) while keeping aspect ratio
    w, h = rgba.size
    scale = OUTPUT_SIZE / max(w, h)
    rgba = rgba.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

    # 3. CLAHE on luminance channel only (keeps color/alpha intact)
    arr = np.array(rgba)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=TILE_GRID)
    l2 = clahe.apply(l)
    lab2 = cv2.merge((l2, a, b))
    rgb2 = cv2.cvtColor(lab2, cv2.COLOR_LAB2RGB)

    out = np.dstack([rgb2, alpha])
    Image.fromarray(out, mode="RGBA").save(dst_path)
    print(f"[prep_photo] wrote {dst_path} ({out.shape[1]}x{out.shape[0]})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python scripts/prep_photo.py <source.jpg> <dest.png>")
        sys.exit(1)
    prep(sys.argv[1], sys.argv[2])
