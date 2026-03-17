"""Config loading helpers for Taiwan Stock Radar demo workflows."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except ModuleNotFoundError:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_project_config(
    project_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    config_dir = project_root / "config"
    settings = load_mapping(config_dir / "settings.yaml")
    weights = load_mapping(config_dir / "weights.yaml")
    universe = load_mapping(config_dir / "universe.yaml")
    action_rules = load_mapping(config_dir / "action_rules.yaml")
    return settings, weights, universe, action_rules


def load_premarket_config(project_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    config_dir = project_root / "config"
    settings = load_mapping(config_dir / "settings.yaml")
    premarket_rules = load_mapping(config_dir / "premarket_rules.yaml")
    return settings, premarket_rules


def load_daily_market_brief_config(
    project_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    config_dir = project_root / "config"
    settings = load_mapping(config_dir / "settings.yaml")
    premarket_rules = load_mapping(config_dir / "premarket_rules.yaml")
    daily_market_brief_rules = load_mapping(config_dir / "daily_market_brief_rules.yaml")
    return settings, premarket_rules, daily_market_brief_rules


def load_single_stock_committee_config(
    project_root: Path,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    config_dir = project_root / "config"
    settings = load_mapping(config_dir / "settings.yaml")
    weights = load_mapping(config_dir / "weights.yaml")
    universe = load_mapping(config_dir / "universe.yaml")
    action_rules = load_mapping(config_dir / "action_rules.yaml")
    indicator_catalog = load_mapping(config_dir / "indicator_catalog.yaml")
    style_weights = load_mapping(config_dir / "style_weights.yaml")
    strategy_modules = load_mapping(config_dir / "strategy_modules.yaml")
    evaluation_metrics = load_mapping(config_dir / "evaluation_metrics.yaml")
    agent_personas = load_mapping(config_dir / "agent_personas.yaml")
    return (
        settings,
        weights,
        universe,
        action_rules,
        indicator_catalog,
        style_weights,
        strategy_modules,
        evaluation_metrics,
        agent_personas,
    )


def resolve_output_dir(project_root: Path, settings: dict[str, Any]) -> Path:
    output_dir = settings.get("paths", {}).get("output_dir", "output")
    return project_root / output_dir
