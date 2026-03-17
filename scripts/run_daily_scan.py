#!/usr/bin/env python3
"""Generate demo-mode Taiwan stock scan outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from taiwan_stock_radar.workflows import generate_market_scan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the demo daily Taiwan radar scan.")
    parser.add_argument("--date", dest="analysis_date", help="Analysis date in YYYY-MM-DD format.")
    parser.add_argument(
        "--regime",
        choices=["bull", "sideways", "bear", "high_volatility"],
        help="Override the configured market regime.",
    )
    parser.add_argument("--top-n", type=int, help="Number of ranked results to export.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = generate_market_scan(
        PROJECT_ROOT,
        analysis_date=args.analysis_date,
        regime=args.regime,
        top_n=args.top_n,
    )
    scan_result = bundle["report"]

    print(f"Generated demo scan for {scan_result['analysis_date']}")
    print(f"Market regime: {scan_result['market_regime']}")
    print(f"Universe size: {scan_result['universe_size']}")
    print(f"Output directory: {bundle['output_dir']}")
    print("Top 5:")
    for index, row in enumerate(scan_result["top20"][:5], start=1):
        print(
            f"{index}. {row['symbol']} {row['name']} | "
            f"Score {row['radar_score']} | {row['direction_bias']} | "
            f"Buy {row['buy_zone']} | Stop {row['stop_loss']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
