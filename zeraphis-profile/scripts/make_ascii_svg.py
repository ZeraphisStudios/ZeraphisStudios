#!/usr/bin/env python3
"""
make_ascii_svg.py — photo -> typing monochrome ASCII portrait (SVG).

Reads source-prepped.png (RGBA, background already removed), converts it to
an ASCII-art grid, and writes avi-ascii.svg: a self-contained SVG that types
itself in row by row using SMIL animation when loaded as a GitHub README
<img>.

Env vars:
    STATIC=1   write the final (fully revealed) frame only, no animation —
               useful for quick previews.

Usage:
    python scripts/make_ascii_svg.py
"""
import os
import numpy as np
from PIL import Image

# ---- tunables ---------------------------------------------------------
SRC = "source-prepped.png"
OUT = "avi-ascii.svg"

COLS = 90                 # ascii grid width in characters
CHAR_ASPECT = 2.15         # terminal chars are taller than wide; corrects sampling
FONT_SIZE = 7
LINE_HEIGHT = FONT_SIZE * 1.05
FONT_FAMILY = "'SFMono-Regular','Consolas','Liberation Mono',monospace"

CONTRAST = 1.15            # post-multiply on normalized brightness
GAMMA = 0.9                # <1 lightens midtones, >1 darkens
WHITE_FLOOR = 0.06         # minimum brightness treated as "not background"

COLOR = "#c9d1d9"          # monochrome light-gray (GitHub dark-mode friendly)
BG = "transparent"

ROW_DUR = 0.045            # seconds each row takes to type in
STAGGER = 0.035            # seconds delay between consecutive rows starting
# ASCII ramp, darkest -> lightest
RAMP = "@%#*+=-:. "
# -------------------------------------------------------------------------


def load_luminance(path: str) -> np.ndarray:
    img = Image.open(path).convert("RGBA")
    arr = np.array(img).astype(np.float32)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3] / 255.0
    lum = (0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]) / 255.0
    # composite onto black background using alpha, so transparent bg -> darkest
    # (mapped to blank space, not a rendered glyph) via WHITE_FLOOR/alpha mask
    return lum, alpha


def to_ascii_grid(lum: np.ndarray, alpha: np.ndarray) -> list[str]:
    h, w = lum.shape
    rows = int(COLS * (h / w) / CHAR_ASPECT)
    rows = max(1, rows)

    # resize via simple PIL for quality
    lum_img = Image.fromarray((lum * 255).astype(np.uint8))
    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8))
    lum_small = np.array(lum_img.resize((COLS, rows), Image.LANCZOS)).astype(np.float32) / 255.0
    alpha_small = np.array(alpha_img.resize((COLS, rows), Image.LANCZOS)).astype(np.float32) / 255.0

    # gamma + contrast
    adj = np.clip(lum_small, 0, 1) ** GAMMA
    adj = np.clip((adj - 0.5) * CONTRAST + 0.5, 0, 1)

    ramp_n = len(RAMP) - 1
    lines = []
    for r in range(rows):
        chars = []
        for c in range(COLS):
            a = alpha_small[r, c]
            if a < WHITE_FLOOR:
                chars.append(" ")
                continue
            v = adj[r, c]
            idx = int(round((1 - v) * ramp_n))
            idx = min(max(idx, 0), ramp_n)
            chars.append(RAMP[idx])
        lines.append("".join(chars))
    return lines


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(lines: list[str], static: bool) -> str:
    n_rows = len(lines)
    n_cols = max(len(l) for l in lines) if lines else 0
    char_w = FONT_SIZE * 0.6
    width = n_cols * char_w + 20
    height = n_rows * LINE_HEIGHT + 20

    text_rows = []
    total_dur = 0.0
    for i, line in enumerate(lines):
        y = 12 + (i + 1) * LINE_HEIGHT
        content = esc(line) if line.strip() else " "
        start = i * STAGGER
        total_dur = max(total_dur, start + ROW_DUR)
        if static:
            text_rows.append(
                f'<text x="10" y="{y:.2f}" xml:space="preserve">{content}</text>'
            )
        else:
            # each row fades/types in via opacity animation, staggered
            text_rows.append(
                f'<text x="10" y="{y:.2f}" xml:space="preserve" opacity="0">'
                f'{content}'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{start:.3f}s" dur="{ROW_DUR:.3f}s" fill="freeze" />'
                f"</text>"
            )

    style = (
        f"text{{font-family:{FONT_FAMILY};font-size:{FONT_SIZE}px;"
        f"fill:{COLOR};white-space:pre;}}"
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" height="{height:.0f}">
<style>{style}</style>
<rect width="100%" height="100%" fill="{BG}"/>
<g>
{''.join(text_rows)}
</g>
</svg>"""
    return svg


def main():
    static = os.environ.get("STATIC") == "1"
    lum, alpha = load_luminance(SRC)
    lines = to_ascii_grid(lum, alpha)
    svg = build_svg(lines, static)
    out = OUT if not static else OUT.replace(".svg", "-static.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"[make_ascii_svg] wrote {out} ({len(lines)} rows)")


if __name__ == "__main__":
    main()
