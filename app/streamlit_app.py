"""Streamlit demo for taiwan-stock-radar."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from taiwan_stock_radar.config import load_project_config, resolve_output_dir
from taiwan_stock_radar.demo_scan import generate_scan_result


def load_scan_payload() -> dict:
    settings, weights, universe, action_rules = load_project_config(PROJECT_ROOT)
    output_dir = resolve_output_dir(PROJECT_ROOT, settings)
    json_path = output_dir / "daily_top20.json"
    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        return {"payload": payload, "settings": settings}
    payload = generate_scan_result(settings, weights, universe, action_rules)
    return {"payload": payload, "settings": settings}


def main() -> None:
    loaded = load_scan_payload()
    payload = loaded["payload"]
    settings = loaded["settings"]
    records = payload["top20"]
    factors = pd.DataFrame(payload["sector_summary"])
    ranking_df = pd.DataFrame(records)
    app_settings = settings.get("app", {})
    project_settings = settings.get("project", {})
    title = app_settings.get("title", project_settings.get("display_name", "Taiwan Stock Radar"))
    subtitle = app_settings.get(
        "subtitle",
        "Indicator-driven single-stock Taiwan equity committee with legacy scan demo support",
    )
    version = project_settings.get("plan_version", "v1.6")

    st.set_page_config(page_title=title, page_icon="📈", layout="wide")
    st.title(title)
    st.caption(f"{subtitle} | Version {version}")
    st.info(payload["disclaimer"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Analysis Date", payload["analysis_date"])
    col2.metric("Market Regime", payload["market_regime"].replace("_", " ").title())
    col3.metric("Universe Size", payload["universe_size"])
    col4.metric("Average Score", payload["average_score"])

    left, right = st.columns([1.6, 1])
    with left:
        st.subheader("Top 20 Radar Ranking")
        display_columns = [
            "symbol",
            "name",
            "sector",
            "radar_score",
            "direction_bias",
            "signal",
            "setup_type",
            "buy_zone",
            "stop_loss",
            "main_risk_flag",
        ]
        st.dataframe(
            ranking_df[display_columns],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.subheader("Signal Distribution")
        signal_df = pd.DataFrame(
            [
                {"signal": signal, "count": count}
                for signal, count in payload["signal_distribution"].items()
            ]
        )
        st.bar_chart(signal_df.set_index("signal"))

        st.subheader("Leading Sectors")
        st.dataframe(factors.head(8), use_container_width=True, hide_index=True)

    st.subheader("Stock Detail")
    selected_symbol = st.selectbox(
        "Select a stock",
        options=ranking_df["symbol"].tolist(),
        format_func=lambda symbol: f"{symbol} {ranking_df.loc[ranking_df['symbol'] == symbol, 'name'].iloc[0]}",
    )
    selected_row = next(row for row in records if row["symbol"] == selected_symbol)
    detail_left, detail_right = st.columns([1.1, 1.4])

    with detail_left:
        st.markdown(f"**{selected_row['symbol']} {selected_row['name']}**")
        st.write(f"Sector: `{selected_row['sector']}`")
        st.write(f"Signal: `{selected_row['signal']}`")
        st.write(f"Direction bias: `{selected_row['direction_bias']}`")
        st.write(f"Setup type: `{selected_row['setup_type']}`")
        st.write(f"Radar score: `{selected_row['radar_score']}`")
        st.write(f"Reference price: `{selected_row['reference_price']}`")
        st.write(f"Buy zone: `{selected_row['buy_zone']}`")
        st.write(f"Stop loss: `{selected_row['stop_loss']}`")
        st.write(f"Take profit 1: `{selected_row['take_profit_1']}`")
        st.write(f"Take profit 2: `{selected_row['take_profit_2']}`")
        st.write(f"Relative strength: `{selected_row['relative_strength']}`")
        st.write(f"Key drivers: {selected_row['key_drivers']}")
        st.write(f"Main risk flag: {selected_row['main_risk_flag']}")
        st.write(f"Next trigger: {selected_row['next_trigger']}")
        st.write(f"Sell plan: {selected_row['sell_plan']}")
        st.write(f"Action note: {selected_row['action_note']}")
        st.write(f"Thesis: {selected_row['thesis']}")

    with detail_right:
        st.markdown("**Factor Breakdown**")
        factor_df = pd.DataFrame(
            [
                {"component": component, "score": score}
                for component, score in selected_row["factor_breakdown"].items()
            ]
        )
        st.bar_chart(factor_df.set_index("component"))

    with st.expander("How to refresh the demo data"):
        st.code("python3 scripts/run_daily_scan.py", language="bash")
        st.code("streamlit run app/streamlit_app.py", language="bash")


if __name__ == "__main__":
    main()
