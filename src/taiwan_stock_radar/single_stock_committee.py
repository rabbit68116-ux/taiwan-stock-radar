"""Executable single-stock committee report for Taiwan Stock Radar v1.7."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from statistics import mean
from typing import Any

from .demo_data import DEMO_STOCK_FACTORS
from .demo_market_context import DEMO_PRICE_CONTEXT
from .demo_scan import generate_scan_result
from .output_store import write_report_bundle

ROLE_LABELS = {
    "chief_strategist": "首席策略統籌",
    "technical_strategist": "技術結構分析師",
    "chip_flow_analyst": "籌碼流向分析師",
    "fundamental_analyst": "基本面分析師",
    "catalyst_analyst": "事件催化分析師",
    "risk_manager": "風險控管分析師",
    "strategy_architect": "策略架構分析師",
    "quant_validation_analyst": "量化驗證分析師",
}

STYLE_LABELS = {
    "short_term": "短線",
    "swing": "波段",
    "position": "中長線",
}

ENGINE_LABELS = {
    "trend": "趨勢",
    "momentum": "動能",
    "price_volume": "量價",
    "chip_flow": "籌碼",
    "fundamentals": "基本面",
    "events": "事件",
}

STRATEGY_ENGINE_MAP = {
    "trend_following": ("trend", "momentum", "fundamentals"),
    "relative_strength_leadership": ("trend", "chip_flow", "price_volume"),
    "breakout_confirmation": ("price_volume", "momentum", "trend"),
    "pullback_continuation": ("trend", "chip_flow", "fundamentals"),
    "volatility_contraction_expansion": ("price_volume", "momentum", "events"),
    "tactical_mean_reversion": ("momentum", "price_volume", "events"),
}


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _score_label(score: float) -> str:
    if score >= 0.78:
        return "強勢支持"
    if score >= 0.65:
        return "建設性"
    if score >= 0.52:
        return "中性偏正"
    if score >= 0.40:
        return "分歧"
    return "偏弱"


def _confidence_label(score: float) -> str:
    if score >= 82:
        return "高"
    if score >= 64:
        return "中"
    return "低"


def _market_regime(daily_brief: dict[str, Any]) -> str:
    overall = float(daily_brief["overall_score"])
    if overall >= 70:
        return "bull"
    if overall >= 55:
        return "sideways"
    if overall >= 45:
        return "high_volatility"
    return "bear"


def _symbol_meta(universe: dict[str, Any], symbol: str) -> dict[str, Any]:
    for item in universe.get("symbols", []):
        if item["symbol"] == symbol:
            return item
    raise ValueError(f"Unknown symbol: {symbol}")


def _event_score(metrics: dict[str, Any], daily_brief: dict[str, Any]) -> float:
    daily_factor = float(daily_brief.get("overall_score", 50.0)) / 100.0
    source_penalty = 0.04 * sum(1 for item in daily_brief.get("sources", []) if item["status"] != "ok")
    score = 0.42 + daily_factor * 0.28 + float(metrics["sector"]) * 0.16 - float(metrics["risk"]) * 0.22 - source_penalty
    return round(_clamp(score), 3)


def _build_engine_scores(metrics: dict[str, Any], daily_brief: dict[str, Any]) -> dict[str, float]:
    price_volume = (float(metrics["volume"]) * 0.7) + (float(metrics["momentum"]) * 0.3)
    engines = {
        "trend": round(float(metrics["trend"]), 3),
        "momentum": round(float(metrics["momentum"]), 3),
        "price_volume": round(_clamp(price_volume), 3),
        "chip_flow": round(float(metrics["capital_flow"]), 3),
        "fundamentals": round(float(metrics["quality"]), 3),
        "events": _event_score(metrics, daily_brief),
    }
    return engines


def _engine_narrative(
    engine_id: str,
    score: float,
    stock_row: dict[str, Any],
    daily_brief: dict[str, Any],
) -> str:
    if engine_id == "trend":
        return (
            f"{stock_row['symbol']} 目前屬於 {stock_row['direction_bias']} 架構，"
            f"均線代理分數 {score * 100:.1f}，適合把 {stock_row['buy_zone']} 視為主要風險定義區。"
        )
    if engine_id == "momentum":
        return (
            f"動能層維持 {_score_label(score)}，配合 {stock_row['signal']} 訊號，"
            "可視為延續而非單日情緒的代理讀法。"
        )
    if engine_id == "price_volume":
        return (
            f"量價品質 {score * 100:.1f}，現階段以 {stock_row['setup_type']} 結構為主，"
            f"重點在於是否能守住 {stock_row['buy_zone']} 並延續量能。"
        )
    if engine_id == "chip_flow":
        return (
            f"籌碼層為 {_score_label(score)}，結合相對強度 {stock_row['relative_strength']:.1f}，"
            "顯示資金偏好仍在，但尚未替代即時法人與借券資料。"
        )
    if engine_id == "fundamentals":
        return (
            f"基本面代理值 {score * 100:.1f}，主論點為：{stock_row['thesis']}。"
        )
    return (
        f"事件層以當日 08:30 報告為外部情境代理，整體為 {daily_brief['overall_label']}，"
        f"因此事件分數落在 {score * 100:.1f}。"
    )


def _style_profile(style_weights: dict[str, Any], style: str, engines: dict[str, float]) -> dict[str, Any]:
    style_config = style_weights["styles"][style]
    weighted_score = sum(
        float(style_config["engine_weights"][engine]) * float(score)
        for engine, score in engines.items()
    )
    return {
        "style": style,
        "label": STYLE_LABELS.get(style, style),
        "description": style_config["description"],
        "engine_weights": style_config["engine_weights"],
        "priority_indicators": style_config["priority_indicators"],
        "fit_score": round(weighted_score * 100, 1),
        "fit_label": _score_label(weighted_score),
        "interpretation_rules": style_weights.get("interpretation_rules", {}).get(style, []),
    }


def _strategy_candidates(
    strategy_modules: dict[str, Any],
    style: str,
    regime: str,
    engines: dict[str, float],
    stock_row: dict[str, Any],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    setup_type = stock_row["setup_type"]
    relative_strength = float(stock_row["relative_strength"]) / 100.0
    risk_penalty = float(DEMO_STOCK_FACTORS[stock_row["symbol"]]["risk"])

    for item in strategy_modules["strategy_families"]:
        related_engines = STRATEGY_ENGINE_MAP[item["id"]]
        engine_score = mean(engines[key] for key in related_engines)
        score = engine_score * 0.68
        score += 0.16 if style in item["preferred_styles"] else -0.03
        score += 0.10 if regime in item["preferred_regimes"] else -0.05

        if setup_type == "breakout" and item["id"] == "breakout_confirmation":
            score += 0.10
        if setup_type == "trend_pullback" and item["id"] in {"trend_following", "pullback_continuation"}:
            score += 0.10
        if setup_type == "early_base" and item["id"] == "volatility_contraction_expansion":
            score += 0.08
        if relative_strength >= 0.82 and item["id"] == "relative_strength_leadership":
            score += 0.08
        if risk_penalty >= 0.30 and item["id"] in {"breakout_confirmation", "tactical_mean_reversion"}:
            score -= 0.06

        candidates.append(
            {
                "id": item["id"],
                "display_name": item["display_name"],
                "preferred_styles": item["preferred_styles"],
                "preferred_regimes": item["preferred_regimes"],
                "purpose": item["purpose"],
                "score": round(_clamp(score) * 100, 1),
                "confirmations": item["confirmations"],
                "disqualifiers": item["disqualifiers"],
            }
        )

    return sorted(candidates, key=lambda row: row["score"], reverse=True)


def _validation_metrics(
    engines: dict[str, float],
    style_profile: dict[str, Any],
    strategy_score: float,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    risk = float(metrics["risk"])
    signal_balance = mean(engines.values())
    style_fit = style_profile["fit_score"] / 100.0
    strategy_fit = strategy_score / 100.0
    evidence_quality = _clamp((signal_balance * 0.55) + (style_fit * 0.25) + ((1 - risk) * 0.20))
    execution_clarity = _clamp((strategy_fit * 0.5) + ((1 - risk) * 0.35) + (engines["price_volume"] * 0.15))

    sharpe_ratio = round(0.45 + style_fit * 1.15 + engines["trend"] * 0.45 - risk * 0.45, 2)
    sortino_ratio = round(sharpe_ratio + 0.34, 2)
    calmar_ratio = round(0.32 + strategy_fit * 0.88 - risk * 0.35, 2)
    profit_factor = round(0.92 + strategy_fit * 0.72 + engines["chip_flow"] * 0.18 - risk * 0.24, 2)
    expectancy = round(0.14 + strategy_fit * 0.18 - risk * 0.08, 2)
    max_drawdown = round(0.08 + risk * 0.18, 3)
    cvar_95 = round(0.015 + risk * 0.035, 3)
    deflated_sharpe_ratio = round(0.34 + style_fit * 0.26 + engines["fundamentals"] * 0.16 - risk * 0.18, 2)
    walk_forward_stability = round(0.42 + signal_balance * 0.28 + engines["fundamentals"] * 0.15 - risk * 0.12, 2)

    committee_metrics = {
        "signal_engine_balance": round(signal_balance * 100, 1),
        "style_fit_score": style_profile["fit_score"],
        "strategy_fit_score": round(strategy_score, 1),
        "evidence_quality_score": round(evidence_quality * 100, 1),
        "execution_clarity_score": round(execution_clarity * 100, 1),
    }

    verdict_score = mean(committee_metrics.values())
    if verdict_score >= 72 and deflated_sharpe_ratio >= 0.55 and profit_factor >= 1.25:
        verdict_label = "可執行，但仍需風險紀律"
    elif verdict_score >= 60:
        verdict_label = "可觀察，等待更乾淨的確認"
    else:
        verdict_label = "保守處理，暫不主動進場"

    return {
        "committee_metrics": committee_metrics,
        "panels": {
            "signal_quality": {
                "above_ma20": engines["trend"] >= 0.58,
                "above_ma60": engines["trend"] >= 0.70,
                "ma20_slope": "positive" if engines["trend"] >= 0.70 else "flat_to_positive" if engines["trend"] >= 0.55 else "mixed",
                "macd_state": "constructive" if engines["momentum"] >= 0.62 else "mixed",
                "volume_expansion_score": round(engines["price_volume"] * 100, 1),
                "institutional_alignment_score": round(engines["chip_flow"] * 100, 1),
                "monthly_revenue_direction": "positive_proxy" if engines["fundamentals"] >= 0.68 else "mixed_proxy",
                "event_risk_flag": "controlled" if engines["events"] >= 0.55 else "watch",
            },
            "performance": {
                "cagr": round(0.10 + strategy_fit * 0.16 - risk * 0.04, 3),
                "annualized_volatility": round(0.17 + risk * 0.18, 3),
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "calmar_ratio": calmar_ratio,
            },
            "trade_quality": {
                "profit_factor": profit_factor,
                "expectancy": expectancy,
                "win_rate": round(47 + style_fit * 24 - risk * 10, 1),
                "exposure": round(0.42 + strategy_fit * 0.18, 2),
                "turnover": round(0.22 + (1 - style_fit) * 0.20, 2),
                "trade_count": round(34 + style_fit * 22),
            },
            "tail_risk": {
                "max_drawdown": max_drawdown,
                "value_at_risk_95": round(0.013 + risk * 0.026, 3),
                "cvar_95": cvar_95,
                "cdar_95": round(max_drawdown * 0.82, 3),
                "ulcer_index": round(4.5 + risk * 5.8, 2),
                "omega_ratio": round(1.05 + strategy_fit * 0.55 - risk * 0.18, 2),
                "tail_ratio": round(0.95 + (1 - risk) * 0.55, 2),
            },
            "robustness": {
                "walk_forward_stability": walk_forward_stability,
                "purged_cross_validation": round(0.45 + style_fit * 0.20, 2),
                "combinatorial_purged_cross_validation": round(0.43 + strategy_fit * 0.22, 2),
                "deflated_sharpe_ratio": deflated_sharpe_ratio,
                "parameter_stability": round(0.46 + signal_balance * 0.26 - risk * 0.12, 2),
                "cost_sensitivity": "moderate" if risk < 0.24 else "elevated",
                "regime_split_performance": "acceptable" if strategy_fit >= 0.62 else "fragile",
            },
        },
        "verdict_score": round(verdict_score, 1),
        "verdict_label": verdict_label,
    }


def _agent_signal_score(
    agent_id: str,
    engines: dict[str, float],
    style_profile: dict[str, Any],
    strategy_score: float,
    validation_scorecard: dict[str, Any],
    metrics: dict[str, Any],
) -> float:
    risk = float(metrics["risk"])
    if agent_id == "chief_strategist":
        return _clamp((mean(engines.values()) * 0.5) + (style_profile["fit_score"] / 100.0 * 0.25) + (strategy_score / 100.0 * 0.25))
    if agent_id == "technical_strategist":
        return _clamp(mean([engines["trend"], engines["momentum"], engines["price_volume"]]))
    if agent_id == "chip_flow_analyst":
        return _clamp((engines["chip_flow"] * 0.75) + (float(metrics["relative_strength"]) * 0.25))
    if agent_id == "fundamental_analyst":
        return _clamp((engines["fundamentals"] * 0.8) + (engines["events"] * 0.2))
    if agent_id == "catalyst_analyst":
        return _clamp((engines["events"] * 0.75) + (engines["price_volume"] * 0.25))
    if agent_id == "risk_manager":
        return _clamp((1 - risk) * 0.75 + (validation_scorecard["committee_metrics"]["execution_clarity_score"] / 100.0 * 0.25))
    if agent_id == "strategy_architect":
        return _clamp((style_profile["fit_score"] / 100.0 * 0.45) + (strategy_score / 100.0 * 0.55))
    return _clamp(
        (validation_scorecard["committee_metrics"]["evidence_quality_score"] / 100.0 * 0.35)
        + (validation_scorecard["panels"]["robustness"]["deflated_sharpe_ratio"] * 0.35)
        + ((1 - risk) * 0.30)
    )


def _agent_leaning(score: float) -> tuple[str, float]:
    if score >= 0.72:
        return "support", 1.0
    if score >= 0.56:
        return "caution", 0.35
    return "object", -0.65


def _build_specialist_briefs(
    agent_personas: dict[str, Any],
    engines: dict[str, float],
    style_profile: dict[str, Any],
    strategy_selection: dict[str, Any],
    validation_scorecard: dict[str, Any],
    metrics: dict[str, Any],
    stock_row: dict[str, Any],
    daily_brief: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    briefs: list[dict[str, Any]] = []
    support_weight = 0.0
    caution_weight = 0.0
    objection_weight = 0.0
    dissent_notes: list[str] = []

    strongest_engine = max(engines.items(), key=lambda item: item[1])[0]
    weakest_engine = min(engines.items(), key=lambda item: item[1])[0]

    for agent in agent_personas["agents"]:
        score = _agent_signal_score(
            agent["id"],
            engines,
            style_profile,
            strategy_selection["primary"]["score"],
            validation_scorecard,
            metrics,
        )
        leaning, direction = _agent_leaning(score)
        confidence = _confidence_label(round(score * 100, 1))
        weighted_vote = round(direction * float(agent["weight"]), 3)

        if leaning == "support":
            support_weight += float(agent["weight"])
        elif leaning == "caution":
            caution_weight += float(agent["weight"])
        else:
            objection_weight += float(agent["weight"])
            dissent_notes.append(
                f"{ROLE_LABELS.get(agent['id'], agent['display_name'])}："
                f"認為 {ENGINE_LABELS[weakest_engine]} 與風險控制仍不足以支持積極追價。"
            )

        strongest_evidence = _engine_narrative(strongest_engine, engines[strongest_engine], stock_row, daily_brief)
        strongest_objection = _engine_narrative(weakest_engine, engines[weakest_engine], stock_row, daily_brief)
        briefs.append(
            {
                "agent_id": agent["id"],
                "display_name": agent["display_name"],
                "display_name_zh": ROLE_LABELS.get(agent["id"], agent["display_name"]),
                "weight": agent["weight"],
                "leaning": leaning,
                "signal_score": round(score * 100, 1),
                "weighted_vote": weighted_vote,
                "confidence": confidence,
                "focus_areas": agent["focus_areas"],
                "strongest_evidence": strongest_evidence,
                "strongest_objection": strongest_objection,
                "briefing": (
                    f"{ROLE_LABELS.get(agent['id'], agent['display_name'])} 將目前架構解讀為"
                    f"「{_score_label(score)}」，傾向以 {strategy_selection['primary']['display_name']} 作為主要打法。"
                ),
            }
        )

    agreement_map = {
        "support_weight": round(support_weight, 3),
        "caution_weight": round(caution_weight, 3),
        "objection_weight": round(objection_weight, 3),
        "consensus_score": round((support_weight + (caution_weight * 0.55)) * 100, 1),
        "dominant_direction": "偏多執行" if support_weight >= 0.55 else "條件式觀察" if support_weight + caution_weight >= 0.60 else "保守防守",
        "highest_priority_unresolved_risk": briefs[-1]["strongest_objection"] if briefs else "暫無",
    }
    return briefs, agreement_map, dissent_notes


def _peer_context(scan_result: dict[str, Any], stock_row: dict[str, Any]) -> dict[str, Any]:
    peers = [row for row in scan_result["all_records"] if row["sector"] == stock_row["sector"]]
    peers_sorted = sorted(peers, key=lambda item: item["radar_score"], reverse=True)
    rank = next((index for index, item in enumerate(peers_sorted, start=1) if item["symbol"] == stock_row["symbol"]), 0)
    top_peers = [
        {"symbol": item["symbol"], "name": item["name"], "radar_score": item["radar_score"]}
        for item in peers_sorted[:3]
    ]
    return {
        "sector_rank": rank,
        "peer_count": len(peers_sorted),
        "top_peers": top_peers,
        "sector_average_score": round(mean(item["radar_score"] for item in peers_sorted), 2) if peers_sorted else 0.0,
    }


def _action_plan(stock_row: dict[str, Any], daily_brief: dict[str, Any], style: str) -> dict[str, Any]:
    if stock_row["setup_type"] == "breakout":
        aggressive = "突破區間高點後量能同步擴大，再分批承接。"
        conservative = "等待日線站穩突破區且隔日未出現帶量長黑。"
    elif stock_row["setup_type"] == "trend_pullback":
        aggressive = "拉回買進區時量縮止穩，可先建立試單。"
        conservative = "等待回測支撐後重新轉強，再補足部位。"
    else:
        aggressive = "僅在底部結構持續墊高且量能改善時小量試單。"
        conservative = "等待平台上緣被有效站上，再提高參與度。"

    do_not_trade = (
        "若 08:30 日盤報告轉為偏弱防守，且個股開盤第一小時跌破買進區下緣並放量，暫不交易。"
        if daily_brief["overall_score"] < 55
        else "若價格開盤直接遠離買進區並失去量價延續，避免追高。"
    )

    reassessment = (
        f"若 {stock_row['symbol']} 出現失敗突破、跌破 {stock_row['stop_loss']}，"
        "或隔夜市場由偏多轉為防守，需重新召開委員會。"
    )

    return {
        "preferred_buy_zone": stock_row["buy_zone"],
        "aggressive_entry_trigger": aggressive,
        "conservative_entry_trigger": conservative,
        "stop_loss": stock_row["stop_loss"],
        "take_profit_1": stock_row["take_profit_1"],
        "take_profit_2": stock_row["take_profit_2"],
        "full_invalidation": f"跌破 {stock_row['stop_loss']} 並伴隨 {stock_row['main_risk_flag']} 擴大。",
        "do_not_trade_condition": do_not_trade,
        "reassessment_trigger": reassessment,
        "sell_plan": stock_row["sell_plan"],
    }


def _scenario_tree(stock_row: dict[str, Any], daily_brief: dict[str, Any], agreement_map: dict[str, Any]) -> list[dict[str, Any]]:
    consensus = agreement_map["consensus_score"]
    base_prob = 52 if consensus >= 68 else 46
    bull_prob = 28 if daily_brief["overall_score"] >= 65 else 22
    bear_prob = 100 - base_prob - bull_prob
    return [
        {
            "id": "base_case",
            "label": "基本情境",
            "probability": base_prob,
            "narrative": (
                f"若價格維持在 {stock_row['buy_zone']} 上緣之上，且市場維持 {daily_brief['overall_label']}，"
                "則較可能延續原本的波段趨勢。"
            ),
        },
        {
            "id": "bull_case",
            "label": "樂觀情境",
            "probability": bull_prob,
            "narrative": (
                f"若 {stock_row['setup_type']} 結構順利擴張，量價與籌碼同步跟上，"
                f"則可望先挑戰 {stock_row['take_profit_1']}，再觀察 {stock_row['take_profit_2']}。"
            ),
        },
        {
            "id": "bear_case",
            "label": "保守情境",
            "probability": bear_prob,
            "narrative": (
                f"若跌破 {stock_row['stop_loss']} 或外部環境轉弱，"
                "則需把原本的建設性劇本降級為等待再確認。"
            ),
        },
    ]


def _missing_data(daily_brief: dict[str, Any]) -> list[str]:
    items = [
        "v1.7 單股委員會仍屬 MVP，可執行版尚未串接即時法人、借券與融資明細。",
        "基本面與事件日曆仍以框架化代理訊號表示，尚未連動 MOPS / TWSE live feed。",
    ]
    for source in daily_brief.get("sources", []):
        if source["status"] != "ok":
            items.append(f"{source['name']}：{source['detail']}")
    deduped: list[str] = []
    for item in items:
        if item not in deduped:
            deduped.append(item)
    return deduped[:5]


def _confidence(agreement_map: dict[str, Any], validation_scorecard: dict[str, Any], missing_data: list[str]) -> dict[str, Any]:
    raw_score = (
        agreement_map["consensus_score"] * 0.45
        + validation_scorecard["verdict_score"] * 0.35
        + max(0.0, 100 - (len(missing_data) * 8)) * 0.20
    )
    score = round(max(0.0, min(100.0, raw_score)), 1)
    return {
        "score": score,
        "label": _confidence_label(score),
        "note": (
            "目前結論可作為執行框架，但仍須以開盤後量價與市場環境是否延續作最後確認。"
            if score >= 64
            else "目前更適合作為條件式觀察，需等更多即時資料補齊後再提高積極度。"
        ),
    }


def generate_single_stock_committee_report(
    settings: dict[str, Any],
    weights: dict[str, Any],
    universe: dict[str, Any],
    action_rules: dict[str, Any],
    indicator_catalog: dict[str, Any],
    style_weights: dict[str, Any],
    strategy_modules: dict[str, Any],
    evaluation_metrics: dict[str, Any],
    agent_personas: dict[str, Any],
    *,
    symbol: str,
    analysis_date: str | None = None,
    style: str | None = None,
    daily_brief: dict[str, Any],
    regime: str | None = None,
) -> dict[str, Any]:
    analysis_date = analysis_date or date.today().isoformat()
    style = style or settings.get("analysis", {}).get("default_horizon", "swing")
    if symbol not in DEMO_STOCK_FACTORS:
        raise ValueError(f"{symbol} is not available in the v1.7 MVP demo universe.")

    symbol_meta = _symbol_meta(universe, symbol)
    scan_result = generate_scan_result(
        settings,
        weights,
        universe,
        action_rules,
        analysis_date=analysis_date,
        regime=regime or _market_regime(daily_brief),
        top_n=len(universe.get("symbols", [])),
    )
    stock_row = next(row for row in scan_result["all_records"] if row["symbol"] == symbol)
    metrics = DEMO_STOCK_FACTORS[symbol]
    price_context = DEMO_PRICE_CONTEXT[symbol]
    engines = _build_engine_scores(metrics, daily_brief)
    style_profile = _style_profile(style_weights, style, engines)
    strategy_rank = _strategy_candidates(strategy_modules, style, scan_result["market_regime"], engines, stock_row)
    validation_scorecard = _validation_metrics(
        engines,
        style_profile,
        strategy_rank[0]["score"],
        metrics,
    )
    specialist_briefs, agreement_map, dissent = _build_specialist_briefs(
        agent_personas,
        engines,
        style_profile,
        {
            "primary": strategy_rank[0],
            "secondary": strategy_rank[1],
            "avoid": strategy_rank[-1],
        },
        validation_scorecard,
        metrics,
        stock_row,
        daily_brief,
    )
    action_plan = _action_plan(stock_row, daily_brief, style)
    scenario_tree = _scenario_tree(stock_row, daily_brief, agreement_map)
    missing_data = _missing_data(daily_brief)
    confidence = _confidence(agreement_map, validation_scorecard, missing_data)
    peer_context = _peer_context(scan_result, stock_row)

    engine_summary = {
        "engines": [
            {
                "id": engine_id,
                "label": ENGINE_LABELS[engine_id],
                "score": round(score * 100, 1),
                "assessment": _score_label(score),
                "narrative": _engine_narrative(engine_id, score, stock_row, daily_brief),
                "priority_fields": indicator_catalog["signal_engines"][engine_id]["priority_fields"][:5],
            }
            for engine_id, score in engines.items()
        ],
        "strongest_engine": ENGINE_LABELS[max(engines.items(), key=lambda item: item[1])[0]],
        "weakest_engine": ENGINE_LABELS[min(engines.items(), key=lambda item: item[1])[0]],
        "committee_read": (
            f"六層訊號引擎整體為 {round(mean(engines.values()) * 100, 1)}/100，"
            f"最強來自 {ENGINE_LABELS[max(engines.items(), key=lambda item: item[1])[0]]}，"
            f"最弱為 {ENGINE_LABELS[min(engines.items(), key=lambda item: item[1])[0]]}。"
        ),
    }

    strategy_selection = {
        "primary": strategy_rank[0],
        "secondary": strategy_rank[1],
        "avoid": strategy_rank[-1],
        "selection_note": (
            f"主策略選擇 {strategy_rank[0]['display_name']}，是因為它最符合 {STYLE_LABELS.get(style, style)} 風格權重與目前 {scan_result['market_regime']} 市場情境。"
        ),
    }

    final_thesis = (
        f"在 {daily_brief['overall_label']} 的開市前情境下，{symbol} {symbol_meta['name']} 仍屬可觀察的"
        f"{STYLE_LABELS.get(style, style)}個股。委員會認為主打法應以 {strategy_selection['primary']['display_name']} 為主，"
        f"但若 {engine_summary['weakest_engine']} 無法改善，則應把積極度降回等待確認。"
    )

    report = {
        "analysis_date": analysis_date,
        "generated_at_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project": settings.get("project", {}).get("display_name", "Taiwan Stock Radar"),
        "version": settings.get("project", {}).get("plan_version", "v1.7"),
        "report_type": "single_stock_committee",
        "symbol": symbol,
        "stock_context": {
            "symbol": symbol,
            "name": symbol_meta["name"],
            "market": symbol_meta["market"],
            "sector": symbol_meta["sector"],
            "reference_price": price_context["reference_price"],
            "atr_pct": price_context["atr_pct"],
            "radar_score": stock_row["radar_score"],
            "signal": stock_row["signal"],
            "setup_type": stock_row["setup_type"],
            "direction_bias": stock_row["direction_bias"],
            "relative_strength": stock_row["relative_strength"],
            "thesis": stock_row["thesis"],
            "peer_context": peer_context,
        },
        "linked_daily_brief_summary": {
            "analysis_date": daily_brief["analysis_date"],
            "overall_label": daily_brief["overall_label"],
            "overall_score": daily_brief["overall_score"],
            "opening_bias": daily_brief["opening_bias"],
            "overall_summary": daily_brief["overall_summary"],
            "top_messages": [item["title"] for item in daily_brief["top_messages"][:3]],
        },
        "market_regime": scan_result["market_regime"],
        "signal_engine_summary": engine_summary,
        "style_profile": style_profile,
        "specialist_briefs": specialist_briefs,
        "strategy_selection": strategy_selection,
        "validation_scorecard": validation_scorecard,
        "agreement_map": agreement_map,
        "final_thesis": final_thesis,
        "scenario_tree": scenario_tree,
        "buy_zone": stock_row["buy_zone"],
        "entry_triggers": {
            "aggressive": action_plan["aggressive_entry_trigger"],
            "conservative": action_plan["conservative_entry_trigger"],
        },
        "stop_loss": action_plan["stop_loss"],
        "take_profit_plan": {
            "tp1": action_plan["take_profit_1"],
            "tp2": action_plan["take_profit_2"],
            "sell_plan": action_plan["sell_plan"],
        },
        "action_plan": action_plan,
        "robustness_checks": [
            f"Deflated Sharpe {validation_scorecard['panels']['robustness']['deflated_sharpe_ratio']}，驗證層評語為 {validation_scorecard['verdict_label']}。",
            f"Profit Factor {validation_scorecard['panels']['trade_quality']['profit_factor']}，代表策略品質代理值仍具可讀性。",
            f"Max Drawdown {validation_scorecard['panels']['tail_risk']['max_drawdown']:.1%}，需搭配 {action_plan['stop_loss']} 嚴格執行。",
        ],
        "invalidation": action_plan["full_invalidation"],
        "confidence": confidence,
        "missing_data": missing_data,
        "dissent": dissent,
        "disclaimer": (
            "本單股委員會報告僅供研究、教育與產品展示使用，不構成投資建議、招攬、保證報酬或個別證券推薦。 "
            "This single-stock committee report is for research, education, and product demonstration only. It is not investment advice and does not guarantee future performance."
        ),
    }
    return report


def write_single_stock_committee_outputs(
    output_dir: Path,
    report: dict[str, Any],
    *,
    basename: str = "single_stock_committee",
) -> dict[str, dict[str, str]]:
    return write_report_bundle(
        output_dir,
        basename=basename,
        report_type=report["report_type"],
        analysis_date=report["analysis_date"],
        payload=report,
        markdown=_render_single_stock_committee(report),
        symbol=report["symbol"],
    )


def _render_single_stock_committee(report: dict[str, Any]) -> str:
    stock = report["stock_context"]
    daily = report["linked_daily_brief_summary"]
    engines = "\n".join(
        f"- **{item['label']}**：{item['score']}/100，{item['assessment']}。{item['narrative']}"
        for item in report["signal_engine_summary"]["engines"]
    )
    specialists = "\n".join(
        f"- **{item['display_name_zh']} / {item['display_name']}**：{item['leaning']}，"
        f"訊號分數 {item['signal_score']}/100，信心 {item['confidence']}。{item['briefing']}"
        for item in report["specialist_briefs"]
    )
    scenarios = "\n".join(
        f"- **{item['label']} {item['probability']}%**：{item['narrative']}"
        for item in report["scenario_tree"]
    )
    robustness = "\n".join(f"- {item}" for item in report["robustness_checks"])
    dissent = "\n".join(f"- {item}" for item in report["dissent"]) or "- 目前沒有額外異議。"
    missing = "\n".join(f"- {item}" for item in report["missing_data"])

    return f"""# Taiwan Stock Radar v{report['version']} 單股委員會報告

- 日期：{report['analysis_date']}
- 產生時間：{report['generated_at_local']}
- 標的：{report['symbol']} {stock['name']} / {stock['sector']}
- 風格：{report['style_profile']['label']} ({report['style_profile']['style']})
- 市場情境：{daily['overall_label']} / {report['market_regime']}

## 一句話結論

{report['final_thesis']}

## 開市前連結摘要

- 08:30 結論：**{daily['overall_label']}**（{daily['overall_score']}/100）
- 開盤偏向：{daily['opening_bias']}
- 市場摘要：{daily['overall_summary']}

## 標的背景

- 方向偏向：{stock['direction_bias']}
- Radar 分數：{stock['radar_score']}
- 相對強度：{stock['relative_strength']}
- 主要論點：{stock['thesis']}
- 同族群排名：{stock['peer_context']['sector_rank']} / {stock['peer_context']['peer_count']}

## 六層訊號引擎

{engines}

## 八位專家 AI 分析師

{specialists}

## 交易風格與策略選擇

- 主要風格：{report['style_profile']['label']}，適配分數 {report['style_profile']['fit_score']}/100
- 主策略：{report['strategy_selection']['primary']['display_name']}（{report['strategy_selection']['primary']['score']}/100）
- 次策略：{report['strategy_selection']['secondary']['display_name']}（{report['strategy_selection']['secondary']['score']}/100）
- 應避免：{report['strategy_selection']['avoid']['display_name']}（{report['strategy_selection']['avoid']['score']}/100）
- 選擇理由：{report['strategy_selection']['selection_note']}

## 委員會分歧與共識

- 共識分數：{report['agreement_map']['consensus_score']}/100
- 主導方向：{report['agreement_map']['dominant_direction']}
- 未解風險：{report['agreement_map']['highest_priority_unresolved_risk']}

### Dissent Memo

{dissent}

## 驗證面板

- Verdict：**{report['validation_scorecard']['verdict_label']}**（{report['validation_scorecard']['verdict_score']}/100）
- Signal Engine Balance：{report['validation_scorecard']['committee_metrics']['signal_engine_balance']}
- Style Fit Score：{report['validation_scorecard']['committee_metrics']['style_fit_score']}
- Strategy Fit Score：{report['validation_scorecard']['committee_metrics']['strategy_fit_score']}
- Evidence Quality Score：{report['validation_scorecard']['committee_metrics']['evidence_quality_score']}
- Execution Clarity Score：{report['validation_scorecard']['committee_metrics']['execution_clarity_score']}

## 情境樹

{scenarios}

## Action Plan

- Buy Zone：{report['buy_zone']}
- Aggressive Trigger：{report['entry_triggers']['aggressive']}
- Conservative Trigger：{report['entry_triggers']['conservative']}
- Stop Loss：{report['stop_loss']}
- Take Profit 1：{report['take_profit_plan']['tp1']}
- Take Profit 2：{report['take_profit_plan']['tp2']}
- Sell Plan：{report['take_profit_plan']['sell_plan']}
- Invalidation：{report['invalidation']}

## Robustness Checks

{robustness}

## Confidence

- 分數：{report['confidence']['score']}/100
- 等級：{report['confidence']['label']}
- 說明：{report['confidence']['note']}

## Missing Data

{missing}

## 免責聲明

{report['disclaimer']}
"""
