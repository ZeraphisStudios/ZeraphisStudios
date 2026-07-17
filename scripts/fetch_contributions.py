#!/usr/bin/env python3
"""
fetch_contributions.py — scrapes real GitHub contribution data with no auth,
by reading the same HTML fragment GitHub's own profile page uses.

Usage:
    GH_PROFILE_USER=yourname python scripts/fetch_contributions.py
Writes:
    data/contributions.json
"""
import os
import re
import sys
import json
import datetime
import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_PROFILE_USER")
OUT = "data/contributions.json"
URL_TMPL = "https://github.com/users/{user}/contributions"


def fetch(user: str) -> list[dict]:
    url = URL_TMPL.format(user=user)
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    # GitHub renders contribution cells as <td> with data-date / data-level,
    # or as <rect> in newer markup depending on rollout; handle both.
    cells = soup.select("td.ContributionCalendar-day, td[data-date]")
    if not cells:
        cells = soup.select("rect[data-date]")

    for cell in cells:
        date = cell.get("data-date")
        level = cell.get("data-level")
        count_attr = cell.get("data-count")
        if date is None:
            continue
        try:
            level = int(level) if level is not None else None
        except ValueError:
            level = None
        try:
            count = int(count_attr) if count_attr is not None else None
        except ValueError:
            count = None

        # GitHub's current markup puts the human-readable count in a sibling
        # <tool-tip> element's text ("3 contributions on May 4th." /
        # "No contributions on July 13th."), not a data attribute. Fall back
        # to parsing that when data-count isn't present.
        if count is None:
            cell_id = cell.get("id")
            tooltip = None
            if cell_id:
                tooltip = soup.find("tool-tip", attrs={"for": cell_id})
            if tooltip is None:
                tooltip = cell.find_next("tool-tip")
            if tooltip is not None:
                text = tooltip.get_text(strip=True)
                if text.lower().startswith("no contributions"):
                    count = 0
                else:
                    m = re.match(r"(\d+)", text)
                    if m:
                        count = int(m.group(1))

        days.append({"date": date, "level": level, "count": count})

    return days


def compute_streaks(days: list[dict]) -> dict:
    days_sorted = sorted(days, key=lambda d: d["date"])
    today = datetime.date.today()

    cur = 0
    best = 0
    running = 0
    for d in days_sorted:
        active = (d.get("count") or 0) > 0 or (d.get("level") or 0) > 0
        if active:
            running += 1
            best = max(best, running)
        else:
            running = 0

    # current streak: walk backwards from most recent day
    for d in reversed(days_sorted):
        active = (d.get("count") or 0) > 0 or (d.get("level") or 0) > 0
        d_date = datetime.date.fromisoformat(d["date"])
        if d_date > today:
            continue
        if active:
            cur += 1
        else:
            break

    total = sum((d.get("count") or 0) for d in days_sorted)
    return {"current_streak": cur, "longest_streak": best, "total_contributions": total}


def main():
    if not USER:
        print("Set GH_PROFILE_USER env var", file=sys.stderr)
        sys.exit(1)

    days = fetch(USER)
    if not days:
        print(
            "[fetch_contributions] WARNING: no contribution cells parsed — "
            "GitHub's markup may have changed, or the profile has no public activity.",
            file=sys.stderr,
        )

    stats = compute_streaks(days)
    payload = {
        "user": USER,
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "days": days,
        "stats": stats,
    }

    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"[fetch_contributions] wrote {OUT} ({len(days)} days, stats={stats})")


if __name__ == "__main__":
    main()
