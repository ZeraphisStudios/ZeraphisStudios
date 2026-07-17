#!/usr/bin/env python3
"""
render_heatmap_svg.py — contributions -> animated activity panel (SVG).

Reads data/contributions.json and writes contrib-heatmap.svg.
"""
import json
import datetime

SRC = "data/contributions.json"
OUT = "contrib-heatmap.svg"

CELL = 12
GAP = 3
PAD_X = 36
PAD_TOP = 92
PAD_BOTTOM = 52
LEFT_LABEL_W = 34
FRAME = 10

# cyan -> blue -> violet, matching identity card
LEVEL_COLORS = ["#121821", "#1e2f4a", "#3557a0", "#4f8adf", "#a37ee8"]

REVEAL_STAGGER = 0.005
REVEAL_DUR = 0.22

FONT_FAMILY = "'SFMono-Regular','Cascadia Code','Consolas','Liberation Mono',monospace"
COLOR_TEXT = "#6b7f9a"
COLOR_STRONG = "#d8e4f4"
COLOR_ACCENT = "#5ec8ff"


def load():
    with open(SRC, encoding="utf-8") as f:
        return json.load(f)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(payload: dict) -> str:
    days = payload["days"]
    stats = payload["stats"]

    by_date = {d["date"]: d for d in days}
    dates_sorted = sorted(by_date.keys())
    if not dates_sorted:
        raise SystemExit("no contribution data to render")

    start = datetime.date.fromisoformat(dates_sorted[0])
    end = datetime.date.fromisoformat(dates_sorted[-1])
    start_aligned = start - datetime.timedelta(days=(start.weekday() + 1) % 7)

    n_days = (end - start_aligned).days + 1
    n_weeks = (n_days + 6) // 7

    grid_w = LEFT_LABEL_W + PAD_X + n_weeks * (CELL + GAP)
    grid_h = PAD_TOP + PAD_BOTTOM + 7 * (CELL + GAP)
    width = grid_w + FRAME * 2
    height = grid_h + FRAME * 2

    cells = []
    order = 0
    month_labels = {}
    for w in range(n_weeks):
        for dow in range(7):
            date = start_aligned + datetime.timedelta(days=w * 7 + dow)
            if date < start or date > end:
                continue
            rec = by_date.get(date.isoformat())
            level = min(max((rec or {}).get("level") or 0, 0), 4)
            color = LEVEL_COLORS[level]

            x = FRAME + LEFT_LABEL_W + PAD_X + w * (CELL + GAP)
            y = FRAME + PAD_TOP + dow * (CELL + GAP)

            if date.day <= 7 and date.month not in month_labels:
                month_labels[date.month] = x

            begin = order * REVEAL_STAGGER
            cells.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin:.3f}s" dur="{REVEAL_DUR:.3f}s" fill="freeze"/>'
                f"</rect>"
            )
            order += 1

    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    labels = []
    for month, x in sorted(month_labels.items(), key=lambda kv: kv[1]):
        labels.append(
            f'<text x="{x}" y="{FRAME + PAD_TOP - 14}" font-size="10" fill="{COLOR_TEXT}">'
            f'{month_names[month]}</text>'
        )

    day_labels = []
    for dow, name in enumerate(["", "Mon", "", "Wed", "", "Fri", ""]):
        if not name:
            continue
        y = FRAME + PAD_TOP + dow * (CELL + GAP) + CELL - 1
        day_labels.append(
            f'<text x="{FRAME + 18}" y="{y}" font-size="9" fill="{COLOR_TEXT}">{name}</text>'
        )

    total = stats.get("total_contributions", 0)
    current = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)

    # stat pills
    pills = []
    pill_data = [
        ("COMMITS", f"{total}"),
        ("STREAK", f"{current}d"),
        ("BEST", f"{longest}d"),
    ]
    px = FRAME + 28
    for title, value in pill_data:
        pw = max(78, len(value) * 10 + 56)
        pills.append(
            f"""<g transform="translate({px} {FRAME + 28})">
  <rect width="{pw}" height="28" rx="8" fill="#101927" stroke="#2a4060"/>
  <text x="12" y="12" font-size="8" letter-spacing="1.4" fill="{COLOR_ACCENT}">{title}</text>
  <text x="12" y="23" font-size="12" font-weight="700" fill="{COLOR_STRONG}">{esc(value)}</text>
</g>"""
        )
        px += pw + 10

    legend_x = width - FRAME - 130
    legend_y = height - FRAME - 22
    legend = [
        f'<text x="{legend_x}" y="{legend_y}" font-size="10" fill="{COLOR_TEXT}">Less</text>'
    ]
    for i, c in enumerate(LEVEL_COLORS):
        lx = legend_x + 34 + i * (CELL + 3)
        legend.append(
            f'<rect x="{lx}" y="{legend_y - CELL + 2}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>'
        )
    legend.append(
        f'<text x="{legend_x + 34 + len(LEVEL_COLORS) * (CELL + 3) + 6}" y="{legend_y}" '
        f'font-size="10" fill="{COLOR_TEXT}">More</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<defs>
  <linearGradient id="hmBorder" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#3dd6ff"/>
    <stop offset="50%" stop-color="#7b6cff"/>
    <stop offset="100%" stop-color="#e06bff"/>
  </linearGradient>
  <linearGradient id="hmPanel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0d1420"/>
    <stop offset="100%" stop-color="#080b12"/>
  </linearGradient>
  <radialGradient id="hmOrb" cx="90%" cy="15%" r="45%">
    <stop offset="0%" stop-color="#6b5cff" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#6b5cff" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>text{{font-family:{FONT_FAMILY};}}</style>

<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="16" fill="none" stroke="url(#hmBorder)" stroke-width="1.5"/>
<rect x="5" y="5" width="{width - 10}" height="{height - 10}" rx="13" fill="url(#hmPanel)"/>
<rect x="5" y="5" width="{width - 10}" height="{height - 10}" rx="13" fill="url(#hmOrb)"/>

<text x="{FRAME + 28}" y="{FRAME + 14}" font-size="9.5" letter-spacing="2.4" fill="{COLOR_ACCENT}">ACTIVITY // SIGNAL</text>
{''.join(pills)}

{''.join(labels)}
{''.join(day_labels)}
<g>{''.join(cells)}</g>
{''.join(legend)}
</svg>
"""


def main():
    payload = load()
    svg = build_svg(payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[render_heatmap_svg] wrote {OUT}")


if __name__ == "__main__":
    main()
