#!/usr/bin/env python3
"""Generate the Taiwan 08:30 daily market brief from live Yahoo and Cnyes pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from taiwan_stock_radar.workflows import generate_daily_market_brief


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the 08:30 Taiwan daily market brief.")
    parser.add_argument("--date", dest="analysis_date", help="Analysis date in YYYY-MM-DD format.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = generate_daily_market_brief(
        PROJECT_ROOT,
        analysis_date=args.analysis_date,
    )
    brief = bundle["report"]

    print(f"Generated daily market brief for {brief['analysis_date']}")
    print(f"Scheduled time: {brief['scheduled_time_local']}")
    print(f"Opening bias: {brief['opening_bias']} ({brief['opening_score']}/100)")
    print(f"Overall assessment: {brief['overall_label']} ({brief['overall_score']}/100)")
    print(f"Output directory: {bundle['output_dir']}")
    print("Top signals:")
    for item in brief["top_messages"][:4]:
        print(f"- [{item['source']}] {item['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
