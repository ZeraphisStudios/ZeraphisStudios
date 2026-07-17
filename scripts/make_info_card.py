#!/usr/bin/env python3
"""
make_info_card.py — Zeraphis Studios identity panel (SVG).

Run:
    python scripts/make_info_card.py
"""

HOST = "github.com/ZeraphisStudios"
OUT = "info-card.svg"

W = 640
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
    "FiveM Scripting",
    "Modern NUI Interfaces",
    "Performance Optimisation",
]

CURRENT = [
    "Building immersive FiveM experiences",
    "Creating responsive websites & applications",
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chip(x: float, y: float, label: str, delay: float) -> str:
    w = max(54, len(label) * 7.4 + 24)
    return f"""<g transform="translate({x:.1f} {y:.1f})">
  <rect width="{w:.1f}" height="24" rx="6" fill="#0e1624" stroke="#2a3d5c" stroke-width="1">
    <animate attributeName="stroke" values="#2a3d5c;#4a7fd4;#2a3d5c" dur="4s" begin="{delay:.1f}s" repeatCount="indefinite"/>
  </rect>
  <circle cx="10" cy="12" r="2.2" fill="#5ec8ff" opacity="0.9"/>
  <text x="18" y="15.5" font-size="10.5" fill="#c8d6ea">{esc(label)}</text>
</g>"""


def build_svg() -> str:
    chips = []
    x, y = 34, 236
    for i, label in enumerate(TECH):
        w = max(54, len(label) * 7.4 + 24)
        if x + w > W - 34:
            x = 34
            y += 34
        chips.append(chip(x, y, label, i * 0.2))
        x += w + 9

    specs_y = y + 48
    specs = [f'<text x="34" y="{specs_y}" class="sec">SPECIALITIES</text>']
    for i, s in enumerate(SPECIALITIES):
        sy = specs_y + 24 + i * 24
        specs.append(
            f"""<g>
  <rect x="34" y="{sy - 13}" width="24" height="18" rx="4" fill="#122033" stroke="#2d4a6e"/>
  <text x="46" y="{sy}" text-anchor="middle" font-size="9" fill="#5ec8ff" font-weight="700">{i + 1:02d}</text>
  <text x="68" y="{sy}" font-size="12" fill="#d0dced">{esc(s)}</text>
</g>"""
        )

    cur_y = specs_y + 24 + len(SPECIALITIES) * 24 + 20
    currents = [f'<text x="34" y="{cur_y}" class="sec">CURRENT</text>']
    for i, c in enumerate(CURRENT):
        currents.append(
            f'<text x="34" y="{cur_y + 22 + i * 20}" font-size="12" fill="#b7c6da">'
            f'<tspan fill="#5ec8ff">▸</tspan>  {esc(c)}</text>'
        )

    id_block = []
    for i, (k, v) in enumerate(IDENTITY):
        iy = 118 + i * 24
        accent = "#8fd4ff" if k == "ROLE" else "#eef3fb"
        weight = "700" if k == "ROLE" else "600"
        id_block.append(
            f"""<text x="34" y="{iy}" font-size="10.5" letter-spacing="1.6" fill="#657890">{k}</text>
<text x="120" y="{iy}" font-size="13.5" fill="{accent}" font-weight="{weight}">{esc(v)}</text>"""
        )

    card_h = cur_y + 22 + len(CURRENT) * 20 + 36

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
    <stop offset="0%" stop-color="#0c121c"/>
    <stop offset="100%" stop-color="#070a10"/>
  </linearGradient>
  <linearGradient id="accentBar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#2a4a8a"/>
    <stop offset="40%" stop-color="#4a8ad4"/>
    <stop offset="70%" stop-color="#7b9cff"/>
    <stop offset="100%" stop-color="#c47cff"/>
  </linearGradient>
  <radialGradient id="orb" cx="85%" cy="12%" r="55%">
    <stop offset="0%" stop-color="#6b5cff" stop-opacity="0.30"/>
    <stop offset="100%" stop-color="#6b5cff" stop-opacity="0"/>
  </radialGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <path d="M0 2h4" stroke="#8eb0ff" stroke-opacity="0.04" stroke-width="1"/>
  </pattern>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2.4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
  text {{ font-family: {FONT}; }}
  .sec {{ font-size: 9px; letter-spacing: 2.4px; fill: #5ec8ff; }}
</style>

<rect x="1" y="1" width="{W - 2}" height="{card_h - 2:.0f}" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="1.6"/>
<rect x="5" y="5" width="{W - 10}" height="{card_h - 10:.0f}" rx="13" fill="url(#panelGrad)"/>
<rect x="5" y="5" width="{W - 10}" height="{card_h - 10:.0f}" rx="13" fill="url(#orb)"/>
<rect x="5" y="5" width="{W - 10}" height="{card_h - 10:.0f}" rx="13" fill="url(#scan)"/>

<path d="M20 48V24h24M{W - 20} 48V24h-24M20 {card_h - 48:.0f}v24h24M{W - 20} {card_h - 48:.0f}v24h-24"
      fill="none" stroke="#5ec8ff" stroke-width="1.5" opacity="0.8" filter="url(#glow)"/>

<circle cx="30" cy="30" r="4" fill="#ff5f7a"/>
<circle cx="46" cy="30" r="4" fill="#ffbd4a"/>
<circle cx="62" cy="30" r="4" fill="#3dd68c"/>
<text x="84" y="34" font-size="10" letter-spacing="1.8" fill="#6b7f9a">ZERAPHIS // IDENTITY</text>
<g transform="translate({W - 118} 20)">
  <rect width="90" height="20" rx="10" fill="#0a1a16" stroke="#1f5a48"/>
  <circle cx="12" cy="10" r="3" fill="#3dd68c" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="22" y="13.5" font-size="9" letter-spacing="1.2" fill="#5ed4a8">ONLINE</text>
</g>

<text x="34" y="68" font-size="14" fill="#5ec8ff" font-weight="700">guest@zeraphisstudios<tspan fill="#5ec8ff"><animate attributeName="opacity" values="1;1;0;0;1" dur="1.05s" repeatCount="indefinite"/>_</tspan></text>
<text x="34" y="88" font-size="11" fill="#6b7f9a">{esc(HOST)}</text>
<rect x="34" y="98" width="{W - 68}" height="2.5" rx="1.25" fill="url(#accentBar)"/>

{chr(10).join(id_block)}

<path d="M34 218 H{W - 34}" stroke="#1e2c42" stroke-dasharray="3 5"/>
<text x="34" y="236" class="sec">TECHNOLOGY</text>
{chr(10).join(chips)}

{chr(10).join(specs)}

{chr(10).join(currents)}

<rect x="34" y="{card_h - 24:.0f}" width="{W - 68}" height="8" rx="4" fill="url(#accentBar)"/>
</svg>
"""


def main() -> None:
    svg = build_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[make_info_card] wrote {OUT}")


if __name__ == "__main__":
    main()
