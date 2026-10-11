import json
import re
from pathlib import Path
from datetime import datetime, timezone

import requests

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "contributions.json"

USERNAME = "Sarthak-S-2005"
URL = f"https://github.com/users/{USERNAME}/contributions"


def main():
    print(f"Fetching public contributions for {USERNAME}...")

    response = requests.get(
        URL,
        headers={"User-Agent": "GitHub-Profile-Heatmap"},
        timeout=30,
    )
    response.raise_for_status()

    pattern = re.compile(
        r'<td[^>]*data-date="(\d{4}-\d{2}-\d{2})"'
        r'[^>]*data-level="(\d+)"[^>]*>'
    )

    contributions = []

    for date, level in pattern.findall(response.text):
        contributions.append({
            "date": date,
            "level": int(level),
        })

    if not contributions:
        raise RuntimeError(
            "No contribution dates were found. "
            "GitHub may have changed its page format."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "contributions": contributions,
    }

    OUTPUT.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    total = len(contributions)
    active_days = sum(
        item["level"] > 0 for item in contributions
    )

    print(f"Saved {total} contribution-calendar days.")
    print(f"Days with contributions: {active_days}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()