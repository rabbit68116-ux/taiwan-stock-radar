"""Demo scan pipeline shared by the CLI script and Streamlit app."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any

from .demo_data import DEMO_STOCK_FACTORS
from .demo_market_context import DEMO_PRICE_CONTEXT

POSITIVE_COMPONENTS = (
    ("trend", "Trend"),
    ("volume", "Volume"),
    ("capital_flow", "Capital Flow"),
    ("quality", "Quality"),
    ("momentum", "Momentum"),
    ("sector", "Sector"),
)


def _clamp_score(score: float) -> float:
    return round(max(0.0, min(100.0, score)), 2)


def _signal_for_score(score: float) -> str:
    if score >= 80:
        return "Strong Buy Watch"
    if score >= 65:
        return "Buy Watch"
    if score >= 50:
        return "Hold"
    if score >= 35:
        return "Sell Watch"
    return "Risk Alert"


def _setup_type(metrics: dict[str, Any]) -> str:
    if metrics["momentum"] >= 0.85 and metrics["volume"] >= 0.70:
        return "breakout"
    if metrics["trend"] >= 0.75 and metrics["risk"] <= 0.25:
        return "trend_pullback"
    return "early_base"


def _direction_bias(score: float, metrics: dict[str, Any]) -> str:
    if score >= 75 and metrics["momentum"] >= 0.85:
        return "Bullish continuation"
    if score >= 65:
        return "Constructive uptrend"
    if score >= 50:
        return "Range to positive bias"
    return "Defensive / avoid"


def _next_trigger(metrics: dict[str, Any]) -> str:
    if metrics["risk"] >= 0.32:
        return "Need cleaner volatility and firmer MA20 support"
    if metrics["volume"] < 0.6:
        return "Watch for volume expansion on the next breakout attempt"
    if metrics["capital_flow"] < 0.62:
        return "Need stronger institutional flow confirmation"
    return "Hold relative strength and avoid failed-breakout selling"


def _fmt_price(value: float) -> str:
    if value >= 1000:
        return f"{value:,.0f}"
    if value >= 100:
        return f"{value:,.1f}"
    return f"{value:,.2f}"


def _action_plan(
    metrics: dict[str, Any],
    action_rules: dict[str, Any],
    score: float,
    signal: str,
    regime: str,
    symbol: str,
) -> dict[str, str]:
    price_context = DEMO_PRICE_CONTEXT[symbol]
    reference_price = float(price_context["reference_price"])
    atr_pct = float(price_context["atr_pct"])
    setup_type = _setup_type(metrics)
    entry_model = action_rules["entry_models"][setup_type]
    stop_mult = (
        action_rules["risk"]["tight_stop_atr_mult"]
        if regime in {"bear", "high_volatility"} or score < 60
        else action_rules["risk"]["stop_atr_mult"]
    )

    buy_min = reference_price * (1 + atr_pct * float(entry_model["buy_min_atr"]))
    buy_max = reference_price * (1 + atr_pct * float(entry_model["buy_max_atr"]))
    stop_loss = min(buy_min, buy_max) - reference_price * atr_pct * float(stop_mult)
    tp1 = reference_price * (1 + atr_pct * float(action_rules["targets"]["tp1_atr_mult"]))
    tp2 = reference_price * (1 + atr_pct * float(action_rules["targets"]["tp2_atr_mult"]))

    if signal in {"Sell Watch", "Risk Alert"}:
        action_note = "No long entry. Wait for structure rebuild or avoid."
    elif setup_type == "breakout":
        action_note = "Buy only if breakout holds with expanding volume."
    elif setup_type == "trend_pullback":
        action_note = "Prefer pullback entries near MA20-style support, not extended chasing."
    else:
        action_note = "Treat as early-base watchlist name until volume and flow improve."

    return {
        "setup_type": setup_type,
        "direction_bias": _direction_bias(score, metrics),
        "reference_price": _fmt_price(reference_price),
        "buy_zone": f"{_fmt_price(min(buy_min, buy_max))} - {_fmt_price(max(buy_min, buy_max))}",
        "stop_loss": _fmt_price(stop_loss),
        "take_profit_1": _fmt_price(tp1),
        "take_profit_2": _fmt_price(tp2),
        "sell_plan": "Trim into TP1, trail under MA20 / failed breakout for the rest.",
        "action_note": action_note,
    }


def _market_component_value(settings: dict[str, Any], regime: str) -> float:
    regime_scores = settings.get("market", {}).get("market_score_by_regime", {})
    return float(regime_scores.get(regime, regime_scores.get("sideways", 0.6)))


def _factor_breakdown(metrics: dict[str, Any], weights: dict[str, Any], market_value: float) -> dict[str, float]:
    breakdown = {
        label: round(float(metrics[key]) * float(weights[key]), 2)
        for key, label in POSITIVE_COMPONENTS
    }
    breakdown["Market"] = round(market_value * float(weights["market"]), 2)
    breakdown["Risk Adjustment"] = round(float(metrics["risk"]) * float(weights["risk_adjustment"]), 2)
    return breakdown


def _driver_summary(breakdown: dict[str, float]) -> str:
    positive = sorted(
        ((name, value) for name, value in breakdown.items() if value > 0 and name != "Market"),
        key=lambda item: item[1],
        reverse=True,
    )
    return ", ".join(name for name, _ in positive[:3])


def generate_scan_result(
    settings: dict[str, Any],
    weights: dict[str, Any],
    universe: dict[str, Any],
    action_rules: dict[str, Any],
    *,
    analysis_date: str | None = None,
    regime: str | None = None,
    top_n: int | None = None,
) -> dict[str, Any]:
    analysis_date = analysis_date or date.today().isoformat()
    regime = regime or settings.get("market", {}).get("default_regime", "sideways")
    top_n = top_n or int(settings.get("scan", {}).get("top_n", 20))
    market_value = _market_component_value(settings, regime)

    records: list[dict[str, Any]] = []
    for symbol_meta in universe.get("symbols", []):
        symbol = symbol_meta["symbol"]
        metrics = DEMO_STOCK_FACTORS.get(symbol)
        if metrics is None:
            continue

        breakdown = _factor_breakdown(metrics, weights, market_value)
        score = _clamp_score(sum(breakdown.values()))
        signal = _signal_for_score(score)
        action_plan = _action_plan(metrics, action_rules, score, signal, regime, symbol)
        records.append(
            {
                "symbol": symbol,
                "name": symbol_meta["name"],
                "market": symbol_meta["market"],
                "sector": symbol_meta["sector"],
                "radar_score": score,
                "signal": signal,
                "relative_strength": round(float(metrics["relative_strength"]) * 100, 1),
                "key_drivers": _driver_summary(breakdown),
                "main_risk_flag": metrics["risk_flags"][0],
                "risk_flags": metrics["risk_flags"],
                "next_trigger": _next_trigger(metrics),
                "thesis": metrics["thesis"],
                "factor_breakdown": breakdown,
                **action_plan,
            }
        )

    ranked = sorted(records, key=lambda item: item["radar_score"], reverse=True)
    top = ranked[:top_n]

    sector_buckets: dict[str, list[float]] = defaultdict(list)
    for row in ranked:
        sector_buckets[row["sector"]].append(row["radar_score"])
    sector_summary = sorted(
        (
            {
                "sector": sector,
                "average_score": round(mean(scores), 2),
                "stock_count": len(scores),
            }
            for sector, scores in sector_buckets.items()
        ),
        key=lambda item: item["average_score"],
        reverse=True,
    )

    signal_distribution = dict(Counter(row["signal"] for row in ranked))
    average_score = round(mean(row["radar_score"] for row in ranked), 2) if ranked else 0.0

    return {
        "analysis_date": analysis_date,
        "mode": settings.get("project", {}).get("mode", "demo"),
        "project": settings.get("project", {}).get("display_name", "Taiwan Stock Radar"),
        "market_regime": regime,
        "top_n": top_n,
        "universe_size": len(ranked),
        "average_score": average_score,
        "signal_distribution": signal_distribution,
        "sector_summary": sector_summary,
        "top20": top,
        "all_records": ranked,
        "disclaimer": "Demo-mode outputs use illustrative factor inputs and are not live market recommendations.",
    }


def write_scan_outputs(output_dir: Path, scan_result: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    top_rows = scan_result["top20"]

    csv_fields = [
        "symbol",
        "name",
        "market",
        "sector",
        "radar_score",
        "direction_bias",
        "signal",
        "setup_type",
        "buy_zone",
        "stop_loss",
        "take_profit_1",
        "take_profit_2",
        "relative_strength",
        "key_drivers",
        "main_risk_flag",
        "next_trigger",
    ]
    with (output_dir / "daily_top20.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for row in top_rows:
            writer.writerow({field: row[field] for field in csv_fields})

    payload = {
        key: value
        for key, value in scan_result.items()
        if key not in {"all_records"}
    }
    with (output_dir / "daily_top20.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    lines = [
        f"# Daily Taiwan Radar Summary ({scan_result['analysis_date']})",
        "",
        f"- Mode: `{scan_result['mode']}`",
        f"- Market regime: `{scan_result['market_regime']}`",
        f"- Universe size: `{scan_result['universe_size']}`",
        f"- Average radar score: `{scan_result['average_score']}`",
        f"- Disclaimer: {scan_result['disclaimer']}",
        "",
        "## Top 20 Watchlist",
        "",
        "| Rank | Symbol | Name | Sector | Radar Score | Direction | Buy Zone | Stop | TP1 | Risk |",
        "|---|---|---|---|---:|---|---|---|---|---|",
    ]
    for index, row in enumerate(top_rows, start=1):
        lines.append(
            f"| {index} | {row['symbol']} | {row['name']} | {row['sector']} | "
            f"{row['radar_score']} | {row['direction_bias']} | {row['buy_zone']} | "
            f"{row['stop_loss']} | {row['take_profit_1']} | {row['main_risk_flag']} |"
        )
    lines.extend(
        [
            "",
            "## Sector Summary",
            "",
            "| Sector | Average Score | Count |",
            "|---|---:|---:|",
        ]
    )
    for sector in scan_result["sector_summary"][:8]:
        lines.append(f"| {sector['sector']} | {sector['average_score']} | {sector['stock_count']} |")

    (output_dir / "daily_summary.md").write_text("\n".join(lines), encoding="utf-8")
