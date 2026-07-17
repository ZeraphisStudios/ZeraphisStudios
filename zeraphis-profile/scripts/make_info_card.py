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
    ("Role", "FiveM Framework Developer"),
    ("Also", "Full Stack Web Developer"),
    ("Focus", "FiveM Systems & Modern Web Applications"),
    ("FiveM", "QBCore \u00b7 Qbox \u00b7 ESX"),
    ("Libraries", "ox_lib \u00b7 ox_inventory \u00b7 ox_target"),
    ("Frontend", "React \u00b7 TypeScript \u00b7 TSX"),
    ("Web", "HTML \u00b7 CSS \u00b7 JavaScript"),
    ("Backend", "Node.js \u00b7 MySQL \u00b7 REST APIs"),
    ("Languages", "Lua \u00b7 JavaScript \u00b7 TypeScript \u00b7 C# \u00b7 Pawn"),
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
COLOR_LABEL = "#8b949e"     # muted gray
COLOR_VALUE = "#c9d1d9"     # light gray
COLOR_ACCENT = "#e6edf3"    # near-white for header/host
COLOR_RULE = "#30363d"
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

    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{HEADER_SIZE}" '
        f'fill="{COLOR_ACCENT}" font-weight="bold">{esc(PROMPT)}</text>'
    )
    y += ROW_H * 0.75
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR_LABEL}">{esc(HOST)}</text>'
    )
    y += ROW_H * 0.6
    parts.append(f'<line x1="{PAD_X}" y1="{y}" x2="{W - PAD_X}" y2="{y}" stroke="{COLOR_RULE}" stroke-width="1"/>')
    y += ROW_H * 0.9

    for label, value in ROWS:
        label_txt = f"{label}:" if label else ""
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR_LABEL}">{esc(label_txt)}</text>'
        )
        parts.append(
            f'<text x="{PAD_X + LABEL_COL_W}" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR_VALUE}">{esc(value)}</text>'
        )
        y += ROW_H

    # small color-swatch row at bottom, neofetch flavor (monochrome ramp, no rainbow)
    y += ROW_H * 0.4
    swatch_w = (W - 2 * PAD_X) / 8
    for i in range(8):
        shade = 40 + i * 22
        color = f"rgb({shade},{shade},{shade})"
        x = PAD_X + i * swatch_w
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{swatch_w - 3:.1f}" height="14" fill="{color}"/>')

    content = "\n".join(parts)
    style = f"text{{font-family:{FONT_FAMILY};}}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{style}</style>
<rect width="100%" height="100%" fill="{BG}"/>
{content}
</svg>"""
    return svg


def main():
    svg = build_svg()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"[make_info_card] wrote {OUT}")


if __name__ == "__main__":
    main()
