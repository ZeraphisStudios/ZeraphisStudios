#!/usr/bin/env python3
"""
make_info_card.py — your experience/stack -> neofetch-style info panel (SVG).

EDIT the ROWS list and HOST string below, then run:
    python scripts/make_info_card.py
to produce info-card.svg.
"""

# ---------------------------------------------------------------------------
# EDIT ME
# ---------------------------------------------------------------------------
HOST = "github.com/ZeraphisStudios"

# (label, value) pairs, rendered in order, neofetch style
ROWS = [
    ("Name", "Zeraphis"),
    ("Role", "FiveM Developer"),
    ("Also", "Web Developer"),
    ("Focus", "FiveM Systems & Modern Web Applications"),
    ("Frontend", "React · TypeScript · TSX"),
    ("Web", "HTML · CSS · JavaScript"),
    ("Backend", "Node.js · MySQL · REST APIs"),
    ("Languages", "Lua · JavaScript · TypeScript · C# · Pawn"),
    ("Specialities", "Framework Compatibility"),
    ("", "Modern NUI Interfaces"),
    ("", "Performance Optimisation"),
    ("Current", "Building immersive FiveM experiences"),
    ("", "Creating responsive web applications"),
]
# ---------------------------------------------------------------------------

OUT = "info-card.svg"

# layout tunables
W = 620
H = 460              # keep in sync with portrait height; bump if content overflows
PAD_X = 26
PAD_TOP = 26
ROW_H = 22
LABEL_COL_W = 150
FONT_FAMILY = "'SFMono-Regular','Consolas','Liberation Mono',monospace"
FONT_SIZE = 13
HEADER_SIZE = 14
COLOR_LABEL = "#7d8b9e"     # muted cool gray
COLOR_VALUE = "#dde6f0"     # cool near-white
COLOR_ACCENT = "#8ab4e8"    # blue accent, echoes the logo
COLOR_RULE = "#28303d"
BG = "transparent"

PROMPT = "guest@zeraphisstudios"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg() -> str:
    parts = []
    y = PAD_TOP

    # header block
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{HEADER_SIZE}" '
        f'fill="{COLOR_ACCENT}" font-weight="bold">{esc(PROMPT)}'
        f'<tspan fill="{COLOR_ACCENT}"><animate attributeName="opacity" '
        f'values="1;1;0;0;1" dur="1.1s" repeatCount="indefinite"/>_</tspan>'
        f"</text>"
    )
    y += ROW_H * 0.75
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR_LABEL}">{esc(HOST)}</text>'
    )
    y += ROW_H * 0.6
    parts.append(
        f'<rect x="{PAD_X}" y="{y - 1}" width="{W - 2 * PAD_X}" height="2" fill="url(#accentGrad)"/>'
    )
    y += ROW_H * 0.95

    section_breaks = {"Specialities", "Current"}
    for i, (label, value) in enumerate(ROWS):
        if label in section_breaks and i > 0:
            y += ROW_H * 0.25
            parts.append(
                f'<line x1="{PAD_X}" y1="{y - ROW_H * 0.6:.1f}" x2="{W - PAD_X}" y2="{y - ROW_H * 0.6:.1f}" '
                f'stroke="{COLOR_RULE}" stroke-width="1" stroke-dasharray="2,3"/>'
            )
        label_txt = f"{label}:" if label else ""
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR_LABEL}">{esc(label_txt)}</text>'
        )
        parts.append(
            f'<text x="{PAD_X + LABEL_COL_W}" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR_VALUE}">{esc(value)}</text>'
        )
        y += ROW_H

    # closing accent bar: a small gradient swatch strip, brand-toned (not grayscale)
    y += ROW_H * 0.35
    parts.append(f'<rect x="{PAD_X}" y="{y}" width="{W - 2 * PAD_X}" height="10" rx="3" fill="url(#swatchGrad)"/>')

    defs = f"""<defs>
<linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#5b7fd6"/>
  <stop offset="55%" stop-color="#8ab4e8"/>
  <stop offset="100%" stop-color="#b48ae0"/>
</linearGradient>
<linearGradient id="swatchGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#2b3550"/>
  <stop offset="40%" stop-color="#4a5fa0"/>
  <stop offset="70%" stop-color="#8ab4e8"/>
  <stop offset="100%" stop-color="#c48ae8"/>
</linearGradient>
</defs>"""

    content = "\n".join(parts)
    style = f"text{{font-family:{FONT_FAMILY};}}"
    card_h = y + 26
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {card_h:.0f}" width="{W}" height="{card_h:.0f}">
<style>{style}</style>
{defs}
<rect width="100%" height="100%" fill="{BG}"/>
<rect x="1" y="1" width="{W - 2}" height="{card_h - 2:.0f}" rx="10" fill="#0d1117" fill-opacity="0.35" stroke="{COLOR_RULE}" stroke-width="1"/>
{content}
</svg>"""
    return svg


def main():
    svg = build_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[make_info_card] wrote {OUT}")


if __name__ == "__main__":
    main()
