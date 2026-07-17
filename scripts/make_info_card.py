#!/usr/bin/env python3
"""
make_info_card.py — Zeraphis Studios identity panel (SVG).

Run:
    python scripts/make_info_card.py
"""

HOST = "github.com/ZeraphisStudios"
OUT = "info-card.svg"

W = 680
FONT = "'SFMono-Regular','Cascadia Code','Consolas','Liberation Mono',monospace"

IDENTITY = [
    ("NAME", "Zeraphis"),
    ("ROLE", "FiveM Developer"),
    ("ALSO", "Web Developer"),
    ("FOCUS", "FiveM Systems & Modern Web"),
]

TECH = [
    "Lua", "React", "TypeScript", "TSX", "JavaScript",
    "HTML", "CSS", "C#", "Pawn", "Node.js", "MySQL",
]

SPECIALITIES = [
    "Framework Compatibility",
    "Modern NUI Interfaces",
    "Performance Optimisation",
]

CURRENT = [
    "Immersive FiveM experiences",
    "Responsive web applications",
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chip(x: float, y: float, label: str, delay: float):
    w = max(58, len(label) * 7.6 + 28)
    svg = f"""<g transform="translate({x:.1f} {y:.1f})">
  <rect width="{w:.1f}" height="28" rx="8" fill="#101927" stroke="#2d4568" stroke-width="1">
    <animate attributeName="stroke" values="#2d4568;#4f86d8;#2d4568" dur="5s" begin="{delay:.1f}s" repeatCount="indefinite"/>
  </rect>
  <circle cx="12" cy="14" r="2.4" fill="#5ec8ff"/>
  <text x="22" y="18" font-size="11" fill="#d2def0">{esc(label)}</text>
</g>"""
    return svg, w


def build_svg() -> str:
    # --- identity block ---
    id_block = []
    for i, (k, v) in enumerate(IDENTITY):
        iy = 124 + i * 30
        accent = "#8fd4ff" if k == "ROLE" else "#eef3fb"
        weight = "700" if k == "ROLE" else "600"
        id_block.append(
            f"""<text x="40" y="{iy}" font-size="11" letter-spacing="1.8" fill="#6a7f99">{k}</text>
<text x="130" y="{iy}" font-size="14" fill="{accent}" font-weight="{weight}">{esc(v)}</text>"""
        )

    # --- technology chips ---
    chips = []
    x, y = 40, 278
    for i, label in enumerate(TECH):
        svg, w = chip(x, y, label, i * 0.18)
        if x + w > W - 40:
            x = 40
            y += 38
            svg, w = chip(x, y, label, i * 0.18)
        chips.append(svg)
        x += w + 12

    # --- two-column lower panels ---
    panel_top = y + 56
    left_x, right_x = 40, 360
    panel_w = 270
    panel_h = 30 + len(SPECIALITIES) * 32 + 16

    specs = [
        f'<rect x="{left_x}" y="{panel_top}" width="{panel_w}" height="{panel_h}" rx="12" fill="#0c1420" stroke="#243652"/>',
        f'<text x="{left_x + 18}" y="{panel_top + 26}" class="sec">SPECIALITIES</text>',
    ]
    for i, s in enumerate(SPECIALITIES):
        sy = panel_top + 48 + i * 32
        specs.append(
            f"""<g>
  <rect x="{left_x + 18}" y="{sy - 14}" width="28" height="22" rx="6" fill="#122033" stroke="#2f4d72"/>
  <text x="{left_x + 32}" y="{sy}" text-anchor="middle" font-size="10" fill="#5ec8ff" font-weight="700">{i + 1:02d}</text>
  <text x="{left_x + 56}" y="{sy}" font-size="12.5" fill="#d4e0f2">{esc(s)}</text>
</g>"""
        )

    currents = [
        f'<rect x="{right_x}" y="{panel_top}" width="{panel_w}" height="{panel_h}" rx="12" fill="#0c1420" stroke="#243652"/>',
        f'<text x="{right_x + 18}" y="{panel_top + 26}" class="sec">CURRENT</text>',
    ]
    for i, c in enumerate(CURRENT):
        cy = panel_top + 52 + i * 36
        currents.append(
            f"""<g>
  <circle cx="{right_x + 26}" cy="{cy - 4}" r="3" fill="#5ec8ff"/>
  <text x="{right_x + 40}" y="{cy}" font-size="12.5" fill="#c8d6ea">{esc(c)}</text>
</g>"""
        )

    card_h = panel_top + panel_h + 48

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {card_h:.0f}" width="{W}" height="{card_h:.0f}">
<defs>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#3dd6ff">
      <animate attributeName="stop-color" values="#3dd6ff;#7b6cff;#e06bff;#3dd6ff" dur="8s" repeatCount="indefinite"/>
    </stop>
    <stop offset="50%" stop-color="#7b6cff">
      <animate attributeName="stop-color" values="#7b6cff;#e06bff;#3dd6ff;#7b6cff" dur="8s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#e06bff">
      <animate attributeName="stop-color" values="#e06bff;#3dd6ff;#7b6cff;#e06bff" dur="8s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0d1420"/>
    <stop offset="100%" stop-color="#080b12"/>
  </linearGradient>
  <linearGradient id="accentBar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#2a4a8a"/>
    <stop offset="40%" stop-color="#4a8ad4"/>
    <stop offset="70%" stop-color="#7b9cff"/>
    <stop offset="100%" stop-color="#c47cff"/>
  </linearGradient>
  <radialGradient id="orb" cx="88%" cy="10%" r="50%">
    <stop offset="0%" stop-color="#6b5cff" stop-opacity="0.26"/>
    <stop offset="100%" stop-color="#6b5cff" stop-opacity="0"/>
  </radialGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <path d="M0 2h4" stroke="#8eb0ff" stroke-opacity="0.035" stroke-width="1"/>
  </pattern>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
  text {{ font-family: {FONT}; }}
  .sec {{ font-size: 9.5px; letter-spacing: 2.6px; fill: #5ec8ff; }}
</style>

<rect x="1" y="1" width="{W - 2}" height="{card_h - 2:.0f}" rx="18" fill="none" stroke="url(#borderGrad)" stroke-width="1.7"/>
<rect x="6" y="6" width="{W - 12}" height="{card_h - 12:.0f}" rx="14" fill="url(#panelGrad)"/>
<rect x="6" y="6" width="{W - 12}" height="{card_h - 12:.0f}" rx="14" fill="url(#orb)"/>
<rect x="6" y="6" width="{W - 12}" height="{card_h - 12:.0f}" rx="14" fill="url(#scan)"/>

<path d="M22 52V28h24M{W - 22} 52V28h-24M22 {card_h - 52:.0f}v24h24M{W - 22} {card_h - 52:.0f}v24h-24"
      fill="none" stroke="#5ec8ff" stroke-width="1.5" opacity="0.75" filter="url(#glow)"/>

<circle cx="34" cy="34" r="4.5" fill="#ff5f7a"/>
<circle cx="52" cy="34" r="4.5" fill="#ffbd4a"/>
<circle cx="70" cy="34" r="4.5" fill="#3dd68c"/>
<text x="94" y="38" font-size="10.5" letter-spacing="2" fill="#6b7f9a">ZERAPHIS // IDENTITY</text>
<g transform="translate({W - 126} 22)">
  <rect width="96" height="22" rx="11" fill="#0a1a16" stroke="#1f5a48"/>
  <circle cx="14" cy="11" r="3.2" fill="#3dd68c" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="26" y="15" font-size="9.5" letter-spacing="1.3" fill="#5ed4a8">ONLINE</text>
</g>

<text x="40" y="78" font-size="15" fill="#5ec8ff" font-weight="700">guest@zeraphisstudios<tspan fill="#5ec8ff"><animate attributeName="opacity" values="1;1;0;0;1" dur="1.05s" repeatCount="indefinite"/>_</tspan></text>
<text x="40" y="100" font-size="12" fill="#6b7f9a">{esc(HOST)}</text>
<rect x="40" y="112" width="{W - 80}" height="2.5" rx="1.25" fill="url(#accentBar)"/>

{chr(10).join(id_block)}

<path d="M40 252 H{W - 40}" stroke="#1e2c42" stroke-dasharray="4 6"/>
<text x="40" y="274" class="sec">TECHNOLOGY</text>
{chr(10).join(chips)}

{chr(10).join(specs)}
{chr(10).join(currents)}

<rect x="40" y="{card_h - 28:.0f}" width="{W - 80}" height="8" rx="4" fill="url(#accentBar)"/>
</svg>
"""


def main() -> None:
    svg = build_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[make_info_card] wrote {OUT}")


if __name__ == "__main__":
    main()
