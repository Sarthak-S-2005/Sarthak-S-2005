import json
import calendar
from pathlib import Path
from datetime import date, timedelta
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

CELL = 13
GAP = 4
LEFT = 65
TOP = 85

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Contribution data not found: {INPUT}"
        )

    data = json.loads(INPUT.read_text(encoding="utf-8"))
    contributions = {
        item["date"]: int(item["level"])
        for item in data["contributions"]
    }

    if not contributions:
        raise ValueError("Contribution data is empty.")

    dates = sorted(contributions)
    start = date.fromisoformat(dates[0])
    end = date.fromisoformat(dates[-1])

    # Align the calendar to start on Sunday.
    start -= timedelta(days=(start.weekday() + 1) % 7)

    weeks = []
    current = start

    while current <= end:
        weeks.append(current)
        current += timedelta(days=7)

    width = LEFT + len(weeks) * (CELL + GAP) + 25
    height = TOP + 7 * (CELL + GAP) + 55

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" '
        'rx="12" fill="#0d1117"/>',
        '<text x="25" y="35" fill="#f0f6fc" '
        'font-family="Arial,sans-serif" font-size="19" '
        'font-weight="bold">GitHub Contribution Activity</text>',
        '<text x="25" y="58" fill="#8b949e" '
        'font-family="Arial,sans-serif" font-size="12">'
        f'{escape(data["username"])} · Public contribution calendar'
        '</text>',
    ]

    month_seen = set()

    for week_index, week_start in enumerate(weeks):
        month_key = (week_start.year, week_start.month)

        if month_key not in month_seen:
            x = LEFT + week_index * (CELL + GAP)
            parts.append(
                f'<text x="{x}" y="77" fill="#8b949e" '
                f'font-family="Arial,sans-serif" font-size="10">'
                f'{calendar.month_abbr[week_start.month]}</text>'
            )
            month_seen.add(month_key)

        for day_index in range(7):
            current_date = week_start + timedelta(days=day_index)

            if current_date > end or current_date < date.fromisoformat(dates[0]):
                continue

            level = contributions.get(current_date.isoformat(), 0)
            level = max(0, min(level, 4))

            x = LEFT + week_index * (CELL + GAP)
            y = TOP + day_index * (CELL + GAP)

            parts.append(
                f'<rect x="{x}" y="{y}" '
                f'width="{CELL}" height="{CELL}" rx="3" '
                f'fill="{COLORS[level]}">'
                f'<title>{current_date.isoformat()}: '
                f'contribution level {level}</title>'
                '</rect>'
            )

    for index, label in enumerate(
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    ):
        y = TOP + index * (CELL + GAP) + 10
        parts.append(
            f'<text x="25" y="{y}" fill="#8b949e" '
            f'font-family="Arial,sans-serif" font-size="10">'
            f'{label}</text>'
        )

    legend_y = height - 24
    parts.append(
        f'<text x="{LEFT}" y="{legend_y}" fill="#8b949e" '
        'font-family="Arial,sans-serif" font-size="10">Less</text>'
    )

    legend_x = LEFT + 35

    for index, color in enumerate(COLORS):
        parts.append(
            f'<rect x="{legend_x + index * 19}" '
            f'y="{legend_y - 10}" width="12" height="12" '
            f'rx="2" fill="{color}"/>'
        )

    parts.append(
        f'<text x="{legend_x + 110}" y="{legend_y}" '
        'fill="#8b949e" font-family="Arial,sans-serif" '
        'font-size="10">More</text>'
    )

    parts.append("</svg>")

    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Heatmap created successfully: {OUTPUT}")


if __name__ == "__main__":
    main()