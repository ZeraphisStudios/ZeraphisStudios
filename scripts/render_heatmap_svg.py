#!/usr/bin/env python3
"""
render_heatmap_svg.py — contributions -> animated GitHub-style box graph.

Reads data/contributions.json (written by fetch_contributions.py) and writes
contrib-heatmap.svg: a self-hosted SVG with a Less->More legend, a real
streak/contribution summary line, and cells that reveal one by one.

Usage:
    python scripts/render_heatmap_svg.py
"""
import json
import datetime

SRC = "data/contributions.json"
OUT = "contrib-heatmap.svg"

CELL = 11
GAP = 3
PAD_X = 20
PAD_TOP = 34
PAD_BOTTOM = 34
LEFT_LABEL_W = 28

# brand-toned level shades (blue -> purple), echoing the logo instead of
# generic GitHub green or flat gray
LEVEL_COLORS = ["#161b22", "#26304a", "#3a4a7a", "#5b7fd6", "#a37ee8"]

REVEAL_STAGGER = 0.006  # seconds between each cell starting to reveal
REVEAL_DUR = 0.25

FONT_FAMILY = "'SFMono-Regular','Consolas','Liberation Mono',monospace"
COLOR_TEXT = "#7d8b9e"
COLOR_TEXT_STRONG = "#dde6f0"


def load():
    with open(SRC) as f:
        return json.load(f)


def build_svg(payload: dict) -> str:
    days = payload["days"]
    stats = payload["stats"]
    user = payload.get("user", "")

    # group by week-column, day-of-week row, same layout as GitHub
    by_date = {d["date"]: d for d in days}
    dates_sorted = sorted(by_date.keys())
    if not dates_sorted:
        raise SystemExit("no contribution data to render")

    start = datetime.date.fromisoformat(dates_sorted[0])
    end = datetime.date.fromisoformat(dates_sorted[-1])

    # align start back to the preceding Sunday so weeks are clean columns
    start_aligned = start - datetime.timedelta(days=(start.weekday() + 1) % 7)

    n_days = (end - start_aligned).days + 1
    n_weeks = (n_days + 6) // 7

    width = LEFT_LABEL_W + PAD_X * 2 + n_weeks * (CELL + GAP)
    height = PAD_TOP + PAD_BOTTOM + 7 * (CELL + GAP)

    cells = []
    order = 0
    month_labels = {}
    for w in range(n_weeks):
        for dow in range(7):
            date = start_aligned + datetime.timedelta(days=w * 7 + dow)
            if date < start or date > end:
                continue
            key = date.isoformat()
            rec = by_date.get(key)
            level = (rec or {}).get("level") or 0
            level = min(max(level, 0), 4)
            color = LEVEL_COLORS[level]

            x = LEFT_LABEL_W + PAD_X + w * (CELL + GAP)
            y = PAD_TOP + dow * (CELL + GAP)

            if date.day <= 7 and date.month not in month_labels:
                month_labels[date.month] = x

            begin = order * REVEAL_STAGGER
            cells.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" ry="2" '
                f'fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin:.3f}s" dur="{REVEAL_DUR:.3f}s" fill="freeze"/>'
                f"</rect>"
            )
            order += 1

    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                    "Aug", "Sep", "Oct", "Nov", "Dec"]
    labels = []
    for month, x in sorted(month_labels.items(), key=lambda kv: kv[1]):
        labels.append(
            f'<text x="{x}" y="{PAD_TOP - 10}" font-size="10" fill="{COLOR_TEXT}">{month_names[month]}</text>'
        )

    day_labels = []
    for dow, name in enumerate(["", "Mon", "", "Wed", "", "Fri", ""]):
        if not name:
            continue
        y = PAD_TOP + dow * (CELL + GAP) + CELL - 2
        day_labels.append(f'<text x="{PAD_X}" y="{y}" font-size="9" fill="{COLOR_TEXT}">{name}</text>')

    # summary line + legend
    summary = (
        f"{stats.get('total_contributions', 0)} contributions \u00b7 "
        f"current streak {stats.get('current_streak', 0)}d \u00b7 "
        f"longest streak {stats.get('longest_streak', 0)}d"
    )
    summary_y = height - 14
    summary_svg = (
        f'<text x="{PAD_X}" y="{summary_y}" font-size="11" fill="{COLOR_TEXT_STRONG}">{summary}</text>'
    )

    legend_x = width - PAD_X - (5 * (CELL + 2)) - 60
    legend_y = summary_y - 4
    legend = [f'<text x="{legend_x}" y="{legend_y}" font-size="10" fill="{COLOR_TEXT}">Less</text>']
    for i, c in enumerate(LEVEL_COLORS):
        lx = legend_x + 32 + i * (CELL + 2)
        legend.append(f'<rect x="{lx}" y="{legend_y - CELL + 2}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
    legend.append(
        f'<text x="{legend_x + 32 + len(LEVEL_COLORS) * (CELL + 2) + 4}" y="{legend_y}" '
        f'font-size="10" fill="{COLOR_TEXT}">More</text>'
    )

    style = f"text{{font-family:{FONT_FAMILY};}}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<style>{style}</style>
<rect width="100%" height="100%" fill="transparent"/>
{''.join(labels)}
{''.join(day_labels)}
<g>{''.join(cells)}</g>
{summary_svg}
{''.join(legend)}
</svg>"""
    return svg


def main():
    payload = load()
    svg = build_svg(payload)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"[render_heatmap_svg] wrote {OUT}")


if __name__ == "__main__":
    main()
