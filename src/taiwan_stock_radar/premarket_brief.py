"""Premarket brief generator for Taiwan night session and US market context."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .demo_premarket_data import DEMO_PREMARKET_PROFILES


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _pct_to_score(change_pct: float, thresholds: dict[str, Any]) -> float:
    strong_positive = float(thresholds["strong_positive_pct"])
    positive = float(thresholds["positive_pct"])
    negative = float(thresholds["negative_pct"])
    strong_negative = float(thresholds["strong_negative_pct"])

    if change_pct >= strong_positive:
        return 1.0
    if change_pct >= positive:
        return 0.75
    if change_pct > negative:
        return 0.5
    if change_pct > strong_negative:
        return 0.25
    return 0.0


def _night_session_score(context: dict[str, Any], rules: dict[str, Any]) -> float:
    thresholds = rules["component_thresholds"]
    change_score = _pct_to_score(float(context["change_pct"]), thresholds)

    volume_ratio = float(context["volume_ratio"])
    if volume_ratio >= float(thresholds["night_volume_ratio_hot"]):
        volume_score = 0.15
    elif volume_ratio <= float(thresholds["night_volume_ratio_soft"]):
        volume_score = -0.1
    else:
        volume_score = 0.0

    return _clamp(change_score + volume_score)


def _broad_us_score(context: dict[str, Any], rules: dict[str, Any]) -> float:
    thresholds = rules["component_thresholds"]
    components = ["sp500", "nasdaq", "dow"]
    values = [_pct_to_score(float(context[item]["change_pct"]), thresholds) for item in components]
    return round(sum(values) / len(values), 4)


def _semi_score(context: dict[str, Any], rules: dict[str, Any]) -> float:
    thresholds = rules["component_thresholds"]
    components = ["sox", "tsm_adr", "nvidia"]
    values = [_pct_to_score(float(context[item]["change_pct"]), thresholds) for item in components]
    return round(sum(values) / len(values), 4)


def _risk_score(context: dict[str, Any], rules: dict[str, Any]) -> float:
    thresholds = rules["component_thresholds"]
    vix_change = float(context["vix"]["change_pct"])
    if vix_change <= float(thresholds["vix_relief_pct"]):
        vix_score = 1.0
    elif vix_change >= float(thresholds["vix_stress_pct"]):
        vix_score = 0.0
    else:
        vix_score = 0.5
    return round(vix_score, 4)


def _opening_bias(score: float, rules: dict[str, Any]) -> tuple[str, str]:
    thresholds = rules["thresholds"]
    if score >= float(thresholds["bullish_open"]):
        return "偏多開盤", "Bullish open bias"
    if score >= float(thresholds["constructive_open"]):
        return "建設性偏強", "Constructive open bias"
    if score >= float(thresholds["neutral_open"]):
        return "中性偏多", "Neutral to mildly positive"
    if score >= float(thresholds["cautious_open"]):
        return "偏保守", "Cautious open bias"
    return "偏空防守", "Defensive / downside risk"


def _opening_plan(score: float, night_change_pct: float, semi_score: float, risk_score: float) -> str:
    if score >= 0.7 and night_change_pct > 0:
        return "預估台股偏高開，早盤若量價延續，電子權值與 AI 鏈有望主導。"
    if score >= 0.58:
        return "預估台股平高開到偏強整理，適合觀察半導體與大型電子能否接棒。"
    if score >= 0.45:
        return "預估台股開盤震盪，夜盤與美股訊號分歧，宜等早盤主線更清楚後再提高積極度。"
    if semi_score < 0.4 or risk_score < 0.35:
        return "預估台股偏弱開出，優先確認權值股與電子期是否持續承壓，避免過早抄底。"
    return "預估台股開盤保守，宜先觀察夜盤缺口是否被回補以及賣壓是否擴散。"


def _sector_watchlist(context: dict[str, Any], scores: dict[str, float]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    us = context["us_markets"]

    if scores["semi"] >= 0.65:
        items.append(
            {
                "sector": "半導體",
                "view": "優先觀察",
                "reason": "SOX、TSM ADR 與 NVIDIA 同步偏強，對台積電、IC 設計與設備鏈有利。",
            }
        )
    if float(us["nasdaq"]["change_pct"]) >= 0.5 and float(us["nvidia"]["change_pct"]) >= 1.0:
        items.append(
            {
                "sector": "AI 伺服器 / 高速運算",
                "view": "偏多觀察",
                "reason": "Nasdaq 與 AI 龍頭延續風險偏好，有利廣達、緯穎、散熱與高速傳輸族群。",
            }
        )
    if float(us["dow"]["change_pct"]) > 0.3 and scores["risk"] >= 0.5:
        items.append(
            {
                "sector": "金融股",
                "view": "中性偏穩",
                "reason": "美股大型權值與風險情緒穩定，有利金融與高股息資金回流。",
            }
        )
    if scores["risk"] < 0.35:
        items.append(
            {
                "sector": "防禦型族群",
                "view": "相對抗跌",
                "reason": "VIX 升溫時，市場更可能回到電信、公用與高股息防禦配置。",
            }
        )
    return items[:3]


def _risk_flags(context: dict[str, Any], scores: dict[str, float]) -> list[str]:
    flags: list[str] = []
    night = context["taiwan_night"]
    us = context["us_markets"]
    if float(night["change_pct"]) < 0 and float(night["volume_ratio"]) >= 1.2:
        flags.append("夜盤下跌且量能放大，代表開盤缺口若失守，賣壓可能延續。")
    if float(us["vix"]["change_pct"]) >= 4.0:
        flags.append("VIX 明顯升高，表示美股風險情緒轉差，台股開盤追價風險上升。")
    if scores["semi"] < 0.4:
        flags.append("半導體領先訊號不足，電子權值開盤若無法接棒，指數容易轉弱。")
    if not flags:
        flags.append("目前沒有明顯外部風險失衡，但仍需確認台股開盤後量價是否延續夜盤訊號。")
    return flags


def _key_drivers(context: dict[str, Any], scores: dict[str, float]) -> list[str]:
    us = context["us_markets"]
    drivers = [
        f"台指期夜盤 {context['taiwan_night']['change_pct']:+.2f}% ，量比 {context['taiwan_night']['volume_ratio']:.2f}",
        f"Nasdaq {us['nasdaq']['change_pct']:+.2f}% / SOX {us['sox']['change_pct']:+.2f}%",
        f"VIX {us['vix']['change_pct']:+.2f}% ，風險分數 {scores['risk']:.2f}",
    ]
    return drivers


def load_premarket_context(
    *,
    profile: str | None = None,
    context_file: str | None = None,
) -> dict[str, Any]:
    if context_file:
        payload = json.loads(Path(context_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Premarket context file must contain a JSON object.")
        return payload

    profile_name = profile or "semi_risk_on"
    try:
        return DEMO_PREMARKET_PROFILES[profile_name]
    except KeyError as exc:
        raise ValueError(f"Unknown premarket profile: {profile_name}") from exc


def generate_premarket_brief(
    settings: dict[str, Any],
    rules: dict[str, Any],
    *,
    analysis_date: str | None = None,
    profile: str | None = None,
    context_file: str | None = None,
) -> dict[str, Any]:
    analysis_date = analysis_date or date.today().isoformat()
    context = load_premarket_context(profile=profile, context_file=context_file)

    weights = rules["weights"]
    taiwan_night_score = _night_session_score(context["taiwan_night"], rules)
    us_broad_score = _broad_us_score(context["us_markets"], rules)
    semi_score = _semi_score(context["us_markets"], rules)
    risk_score = _risk_score(context["us_markets"], rules)

    opening_score = round(
        taiwan_night_score * float(weights["taiwan_night"])
        + us_broad_score * float(weights["us_broad"])
        + semi_score * float(weights["semiconductors"])
        + risk_score * float(weights["risk"]),
        4,
    )
    opening_bias, opening_bias_en = _opening_bias(opening_score, rules)
    sector_watchlist = _sector_watchlist(
        context,
        {"semi": semi_score, "risk": risk_score},
    )
    risk_flags = _risk_flags(
        context,
        {"semi": semi_score, "risk": risk_score},
    )
    key_drivers = _key_drivers(
        context,
        {"risk": risk_score},
    )

    return {
        "analysis_date": analysis_date,
        "project": settings.get("project", {}).get("display_name", "Taiwan Stock Radar"),
        "version": settings.get("project", {}).get("plan_version", "v1.5"),
        "report_type": "premarket_opening_bias",
        "profile_label": context.get("profile_label", profile or "custom"),
        "opening_bias": opening_bias,
        "opening_bias_en": opening_bias_en,
        "opening_score": round(opening_score * 100, 1),
        "expected_opening_plan": _opening_plan(
            opening_score,
            float(context["taiwan_night"]["change_pct"]),
            semi_score,
            risk_score,
        ),
        "taiwan_night": context["taiwan_night"],
        "us_markets": context["us_markets"],
        "macro": context.get("macro", {}),
        "component_scores": {
            "taiwan_night": round(taiwan_night_score, 3),
            "us_broad": round(us_broad_score, 3),
            "semiconductors": round(semi_score, 3),
            "risk": round(risk_score, 3),
        },
        "key_drivers": key_drivers,
        "sector_watchlist": sector_watchlist,
        "risk_flags": risk_flags,
        "disclaimer": (
            "This premarket brief is for research and planning use. "
            "It does not guarantee how Taiwan equities will open or trade intraday."
        ),
    }


def write_premarket_outputs(output_dir: Path, brief: dict[str, Any], basename: str = "premarket_brief") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{basename}.json").write_text(
        json.dumps(brief, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / f"{basename}.md").write_text(_render_markdown_report(brief), encoding="utf-8")


def _render_markdown_report(brief: dict[str, Any]) -> str:
    taiwan_night = brief["taiwan_night"]
    us = brief["us_markets"]
    sectors = brief["sector_watchlist"]
    flags = brief["risk_flags"]

    sector_lines = "\n".join(
        f"- **{item['sector']}**：{item['view']}。{item['reason']}" for item in sectors
    ) or "- 目前沒有明確領先族群，建議等開盤前 15 分鐘再確認。"

    risk_lines = "\n".join(f"- {item}" for item in flags)
    driver_lines = "\n".join(f"- {item}" for item in brief["key_drivers"])

    us_lines = "\n".join(
        f"- **{item['label']}**：{item['change_pct']:+.2f}%"
        for item in [us["sp500"], us["nasdaq"], us["dow"], us["sox"], us["tsm_adr"], us["nvidia"], us["vix"]]
    )

    return f"""# Taiwan Stock Radar v{brief['version']} 開市前趨勢報告

- 日期：{brief['analysis_date']}
- 模式：台股夜盤 + 美股趨勢 + 隔日開市評估
- 情境標籤：{brief['profile_label']}

## 開盤偏向

- **評估結論**：{brief['opening_bias']} ({brief['opening_score']:.1f} / 100)
- **開盤劇本**：{brief['expected_opening_plan']}

## 台股夜盤摘要

- **合約**：{taiwan_night['contract']}
- **收盤 / 變動**：{taiwan_night['last_price']:.1f} / {taiwan_night['change_points']:+.1f} 點 ({taiwan_night['change_pct']:+.2f}%)
- **量比**：{taiwan_night['volume_ratio']:.2f}
- **盤勢觀察**：{taiwan_night['breadth_note']}

## 美股與風險資產摘要

{us_lines}

## 開盤前主要驅動

{driver_lines}

## 優先觀察族群

{sector_lines}

## 風險提醒

{risk_lines}

## 評估說明

- 開市前評估會將 **台股夜盤、S&P 500 / Nasdaq / SOX、TSM ADR / NVIDIA、VIX** 轉成加權分數。
- 這份報告的重點不是預言開盤點數，而是幫助你在 08:00 到 09:00 之間先知道市場偏向 **風險偏好、分化整理，還是防守開盤**。
- 開盤後仍需確認台指現貨、權值股與量價是否延續夜盤與美股訊號，避免只憑外盤單一方向下結論。

## 免責聲明

{brief['disclaimer']}
"""
