#!/usr/bin/env python3
"""Generate the executable single-stock committee report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from taiwan_stock_radar.workflows import generate_single_stock_committee_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the v1.7 single-stock committee workflow.")
    parser.add_argument("--symbol", required=True, help="Taiwan stock symbol in the demo universe.")
    parser.add_argument("--date", dest="analysis_date", help="Analysis date in YYYY-MM-DD format.")
    parser.add_argument(
        "--style",
        choices=["short_term", "swing", "position"],
        default="swing",
        help="Trading style profile to activate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = generate_single_stock_committee_report(
        PROJECT_ROOT,
        symbol=args.symbol,
        analysis_date=args.analysis_date,
        style=args.style,
    )
    report = bundle["report"]

    print(f"Generated single-stock committee report for {report['analysis_date']}")
    print(f"Symbol: {report['symbol']} {report['stock_context']['name']}")
    print(f"Style: {report['style_profile']['label']} ({report['style_profile']['fit_score']}/100)")
    print(f"Market regime: {report['market_regime']}")
    print(f"Final thesis: {report['final_thesis']}")
    print(f"Buy zone: {report['buy_zone']}")
    print(f"Stop loss: {report['stop_loss']}")
    print(f"Take profit: {report['take_profit_plan']['tp1']} / {report['take_profit_plan']['tp2']}")
    print(f"Output directory: {bundle['output_dir']}")
    if "generated_daily_brief" in bundle:
        print("Daily brief was missing for the requested date and has been generated automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
