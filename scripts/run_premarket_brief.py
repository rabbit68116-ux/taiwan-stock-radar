#!/usr/bin/env python3
"""Generate a premarket Taiwan night-session and US-market opening-bias brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from taiwan_stock_radar.config import load_premarket_config, resolve_output_dir
from taiwan_stock_radar.demo_premarket_data import DEMO_PREMARKET_PROFILES
from taiwan_stock_radar.premarket_brief import generate_premarket_brief, write_premarket_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Taiwan premarket night-session brief.")
    parser.add_argument("--date", dest="analysis_date", help="Analysis date in YYYY-MM-DD format.")
    parser.add_argument(
        "--profile",
        choices=sorted(DEMO_PREMARKET_PROFILES),
        help="Use a built-in illustrative market profile.",
    )
    parser.add_argument(
        "--context-file",
        help="Optional JSON file with real premarket context using the same schema as the demo profiles.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings, premarket_rules = load_premarket_config(PROJECT_ROOT)
    output_dir = resolve_output_dir(PROJECT_ROOT, settings)
    basename = premarket_rules.get("report_defaults", {}).get("output_basename", "premarket_brief")

    brief = generate_premarket_brief(
        settings,
        premarket_rules,
        analysis_date=args.analysis_date,
        profile=args.profile or premarket_rules.get("report_defaults", {}).get("default_profile"),
        context_file=args.context_file,
    )
    write_premarket_outputs(output_dir, brief, basename=basename)

    print(f"Generated premarket brief for {brief['analysis_date']}")
    print(f"Opening bias: {brief['opening_bias']} ({brief['opening_score']}/100)")
    print(f"Profile: {brief['profile_label']}")
    print(f"Output directory: {output_dir}")
    print("Key drivers:")
    for item in brief["key_drivers"]:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
