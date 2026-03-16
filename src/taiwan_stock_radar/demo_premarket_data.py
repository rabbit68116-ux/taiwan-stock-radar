"""Illustrative premarket context for Taiwan night-session and US-market briefs."""

from __future__ import annotations

DEMO_PREMARKET_PROFILES = {
    "semi_risk_on": {
        "profile_label": "半導體領漲的風險偏好盤",
        "taiwan_night": {
            "contract": "台指期近月",
            "last_price": 22468.0,
            "change_points": 132.0,
            "change_pct": 0.59,
            "volume_ratio": 1.24,
            "breadth_note": "電子期與台指期同步走高，夜盤買方主導",
        },
        "us_markets": {
            "sp500": {"label": "S&P 500", "change_pct": 0.74},
            "nasdaq": {"label": "Nasdaq", "change_pct": 1.18},
            "dow": {"label": "Dow Jones", "change_pct": 0.36},
            "sox": {"label": "SOX", "change_pct": 2.05},
            "tsm_adr": {"label": "TSM ADR", "change_pct": 1.67},
            "nvidia": {"label": "NVIDIA", "change_pct": 2.91},
            "vix": {"label": "VIX", "change_pct": -6.8},
        },
        "macro": {
            "usd_twd_bias": "穩定偏強",
            "ust10y_change_bps": -3.4,
            "oil_change_pct": 0.2,
        },
    },
    "mixed_rotation": {
        "profile_label": "美股分化、夜盤小幅偏正向",
        "taiwan_night": {
            "contract": "台指期近月",
            "last_price": 22318.0,
            "change_points": 38.0,
            "change_pct": 0.17,
            "volume_ratio": 0.92,
            "breadth_note": "夜盤偏狹幅整理，指數有撐但追價力道不足",
        },
        "us_markets": {
            "sp500": {"label": "S&P 500", "change_pct": 0.18},
            "nasdaq": {"label": "Nasdaq", "change_pct": -0.09},
            "dow": {"label": "Dow Jones", "change_pct": 0.44},
            "sox": {"label": "SOX", "change_pct": 0.31},
            "tsm_adr": {"label": "TSM ADR", "change_pct": 0.22},
            "nvidia": {"label": "NVIDIA", "change_pct": -0.41},
            "vix": {"label": "VIX", "change_pct": 1.9},
        },
        "macro": {
            "usd_twd_bias": "中性",
            "ust10y_change_bps": 1.1,
            "oil_change_pct": 0.4,
        },
    },
    "risk_off_gap_down": {
        "profile_label": "夜盤轉弱、風險資產同步承壓",
        "taiwan_night": {
            "contract": "台指期近月",
            "last_price": 21936.0,
            "change_points": -214.0,
            "change_pct": -0.97,
            "volume_ratio": 1.33,
            "breadth_note": "夜盤賣壓集中，電子期與金融期同步走弱",
        },
        "us_markets": {
            "sp500": {"label": "S&P 500", "change_pct": -1.14},
            "nasdaq": {"label": "Nasdaq", "change_pct": -1.82},
            "dow": {"label": "Dow Jones", "change_pct": -0.88},
            "sox": {"label": "SOX", "change_pct": -2.46},
            "tsm_adr": {"label": "TSM ADR", "change_pct": -2.13},
            "nvidia": {"label": "NVIDIA", "change_pct": -3.28},
            "vix": {"label": "VIX", "change_pct": 11.6},
        },
        "macro": {
            "usd_twd_bias": "美元轉強",
            "ust10y_change_bps": 7.2,
            "oil_change_pct": -1.3,
        },
    },
}
