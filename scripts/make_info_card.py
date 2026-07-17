#!/usr/bin/env python3
"""Generate the animated Zeraphis Studios profile card."""

HOST = "github.com/ZeraphisStudios"
OUT = "info-card.svg"

W = 700
H = 460
FONT_FAMILY = "'SFMono-Regular','Cascadia Code','Consolas','Liberation Mono',monospace"

TECH_ROWS = [
    ["Lua", "React", "TypeScript", "TSX"],
    ["JavaScript", "HTML", "CSS", "C#"],
    ["Pawn", "Node.js", "MySQL"],
]

SPECIALITIES = [
    ("01", "Immersive FiveM systems"),
    ("02", "Modern NUI interfaces"),
    ("03", "Performance optimisation"),
]


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def pill(x: int, y: int, label: str) -> str:
    width = max(62, len(label) * 8 + 28)
    return f"""
<g transform="translate({x} {y})">
  <rect width="{width}" height="27" rx="7" fill="#111a2b" stroke="#273a59"/>
  <circle cx="13" cy="13.5" r="2.5" fill="#68d8ff"/>
  <text x="23" y="18" class="pill">{esc(label)}</text>
</g>"""


def build_svg() -> str:
    tech = []
    for row_index, row in enumerate(TECH_ROWS):
        x = 43
        y = 253 + row_index * 38
        for label in row:
            tech.append(pill(x, y, label))
            x += max(62, len(label) * 8 + 28) + 9

    speciality = []
    for index, (number, label) in enumerate(SPECIALITIES):
        y = 248 + index * 43
        speciality.append(
            f"""<g transform="translate(414 {y})">
  <rect width="31" height="24" rx="6" fill="#16223a" stroke="#385380"/>
  <text x="15.5" y="16.5" text-anchor="middle" class="number">{number}</text>
  <text x="44" y="16.5" class="speciality">{esc(label)}</text>
</g>"""
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#60dfff"/>
    <stop offset=".48" stop-color="#6f8cff"/>
    <stop offset="1" stop-color="#d66bff"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="#111a2b"/>
    <stop offset="1" stop-color="#090e18"/>
  </linearGradient>
  <radialGradient id="glow">
    <stop stop-color="#795cff" stop-opacity=".34"/>
    <stop offset="1" stop-color="#795cff" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#7691c8" stroke-opacity=".055"/>
  </pattern>
  <filter id="blur"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="softGlow">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
  text{{font-family:{FONT_FAMILY};}}
  .micro{{font-size:9px;letter-spacing:1.5px;fill:#7284a4}}
  .label{{font-size:10px;letter-spacing:1.5px;fill:#7183a2}}
  .value{{font-size:13px;fill:#e8f0ff}}
  .pill{{font-size:10.5px;fill:#cbd9ef}}
  .number{{font-size:9px;font-weight:700;fill:#7de2ff}}
  .speciality{{font-size:10.5px;fill:#cbd9ef}}
</style>

<rect x="1" y="1" width="698" height="458" rx="18" fill="#070b12" stroke="#263752"/>
<rect x="2" y="2" width="696" height="456" rx="17" fill="url(#grid)"/>
<circle cx="591" cy="93" r="146" fill="url(#glow)" filter="url(#blur)">
  <animate attributeName="opacity" values=".45;.8;.45" dur="5s" repeatCount="indefinite"/>
</circle>

<!-- precision corner accents -->
<path d="M18 57V27Q18 18 27 18H58M642 18H673Q682 18 682 27V57M18 403V433Q18 442 27 442H58M642 442H673Q682 442 682 433V403"
      fill="none" stroke="url(#frame)" stroke-width="1.5" opacity=".9"/>

<!-- window chrome -->
<circle cx="33" cy="35" r="4" fill="#ff6b87"/>
<circle cx="49" cy="35" r="4" fill="#ffc15c"/>
<circle cx="65" cy="35" r="4" fill="#59e39d"/>
<text x="88" y="39" class="micro">ZERAPHIS_OS / IDENTITY_NODE</text>
<g transform="translate(555 25)">
  <rect width="112" height="21" rx="10.5" fill="#0c1f1c" stroke="#1f574b"/>
  <circle cx="14" cy="10.5" r="3" fill="#62f5bb" filter="url(#softGlow)">
    <animate attributeName="opacity" values="1;.3;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="25" y="14" font-size="8.5" letter-spacing="1.2" fill="#75dcba">AVAILABLE</text>
</g>
<path d="M18 57H682" stroke="#1c2940"/>

<!-- hero identity -->
<text x="42" y="90" font-size="11" letter-spacing="2.2" fill="#6fdfff">PROFILE / 001</text>
<text x="42" y="128" font-size="29" font-weight="700" fill="#f0f5ff">ZERAPHIS<tspan fill="url(#frame)">_</tspan></text>
<text x="42" y="151" font-size="10.5" letter-spacing="1.4" fill="#7588a9">{esc(HOST)}</text>

<g transform="translate(401 79)">
  <path d="M0 0H257V92H0Z" fill="url(#panel)" stroke="#253754"/>
  <path d="M0 0H4V92H0Z" fill="url(#frame)"/>
  <text x="22" y="24" class="label">PRIMARY ROLE</text>
  <text x="22" y="46" class="value">FiveM Developer</text>
  <text x="22" y="67" class="label">SECONDARY ROLE</text>
  <text x="22" y="87" class="value">Web Developer</text>
</g>

<path d="M42 183H658" stroke="#22314a"/>
<circle cx="42" cy="183" r="2.5" fill="#68d8ff"/>
<circle cx="658" cy="183" r="2.5" fill="#ca72ff"/>

<!-- content panels -->
<g transform="translate(25 204)">
  <rect width="364" height="166" rx="12" fill="#0b111d" stroke="#202f48"/>
  <text x="18" y="26" class="label">TECHNOLOGY MATRIX</text>
  <text x="337" y="26" text-anchor="end" class="micro">11 MODULES</text>
</g>
{''.join(tech)}

<g transform="translate(401 204)">
  <rect width="274" height="166" rx="12" fill="#0b111d" stroke="#202f48"/>
  <text x="18" y="26" class="label">CORE CAPABILITIES</text>
</g>
{''.join(speciality)}

<!-- active mission -->
<g transform="translate(25 387)">
  <rect width="650" height="46" rx="11" fill="url(#panel)" stroke="#293b5a"/>
  <rect x="1" y="1" width="5" height="44" rx="3" fill="url(#frame)"/>
  <text x="22" y="18" class="micro">CURRENT MISSION</text>
  <text x="22" y="34" font-size="10.5" fill="#d9e5fa">Building immersive FiveM experiences + responsive web applications</text>
  <text x="628" y="28" text-anchor="end" font-size="18" fill="#5c79a7">↗</text>
</g>
</svg>"""


def main():
    svg = build_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[make_info_card] wrote {OUT}")


if __name__ == "__main__":
    main()
