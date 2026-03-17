"""Shared workflows for CLI, skill flows, and the Windows desktop app."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from .config import (
    load_daily_market_brief_config,
    load_premarket_config,
    load_project_config,
    load_single_stock_committee_config,
    resolve_output_dir,
)
from .daily_market_brief import (
    generate_daily_market_brief as _generate_daily_market_brief_core,
    write_daily_market_brief_outputs,
)
from .demo_scan import generate_scan_result, write_scan_outputs
from .output_store import archive_output_files, list_archive_entries, load_saved_report, latest_output_paths
from .premarket_brief import generate_premarket_brief as _generate_premarket_brief_core
from .premarket_brief import write_premarket_outputs
from .single_stock_committee import (
    generate_single_stock_committee_report as _generate_single_stock_committee_core,
    write_single_stock_committee_outputs,
)


def _bundle(report: dict[str, Any], output_dir: Path, latest: dict[str, str], archive: dict[str, str]) -> dict[str, Any]:
    return {
        "report": report,
        "output_dir": str(output_dir),
        "latest_outputs": latest,
        "archive_outputs": archive,
    }


def generate_premarket_brief(
    project_root: Path,
    *,
    analysis_date: str | None = None,
    profile: str | None = None,
    context_file: str | None = None,
    output_root: Path | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    settings, premarket_rules = load_premarket_config(project_root)
    output_dir = resolve_output_dir(output_root or project_root, settings)
    basename = premarket_rules.get("report_defaults", {}).get("output_basename", "premarket_brief")
    report = _generate_premarket_brief_core(
        settings,
        premarket_rules,
        analysis_date=analysis_date,
        profile=profile or premarket_rules.get("report_defaults", {}).get("default_profile"),
        context_file=context_file,
    )

    latest: dict[str, str] = {}
    archive: dict[str, str] = {}
    if persist:
        write_premarket_outputs(output_dir, report, basename=basename)
        latest = latest_output_paths(output_dir, basename, ("json", "md"))
        archive = archive_output_files(
            output_dir,
            report_type=report["report_type"],
            analysis_date=report["analysis_date"],
            basenames=[basename],
            extensions=("json", "md"),
        )
    return _bundle(report, output_dir, latest, archive)


def generate_daily_market_brief(
    project_root: Path,
    *,
    analysis_date: str | None = None,
    output_root: Path | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    settings, premarket_rules, daily_rules = load_daily_market_brief_config(project_root)
    output_dir = resolve_output_dir(output_root or project_root, settings)
    basename = settings.get("daily_market_brief", {}).get("output_basename", "daily_market_brief")
    report = _generate_daily_market_brief_core(
        settings,
        premarket_rules,
        daily_rules,
        analysis_date=analysis_date,
    )

    latest: dict[str, str] = {}
    archive: dict[str, str] = {}
    if persist:
        write_daily_market_brief_outputs(output_dir, report, basename=basename)
        latest = latest_output_paths(output_dir, basename, ("json", "md"))
        archive = archive_output_files(
            output_dir,
            report_type=report["report_type"],
            analysis_date=report["analysis_date"],
            basenames=[basename],
            extensions=("json", "md"),
        )
    return _bundle(report, output_dir, latest, archive)


def generate_market_scan(
    project_root: Path,
    *,
    analysis_date: str | None = None,
    regime: str | None = None,
    top_n: int | None = None,
    output_root: Path | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    settings, weights, universe, action_rules = load_project_config(project_root)
    output_dir = resolve_output_dir(output_root or project_root, settings)
    report = generate_scan_result(
        settings,
        weights,
        universe,
        action_rules,
        analysis_date=analysis_date,
        regime=regime,
        top_n=top_n,
    )
    report["report_type"] = "market_scan"

    latest: dict[str, str] = {}
    archive: dict[str, str] = {}
    if persist:
        write_scan_outputs(output_dir, report)
        latest = {
            **latest_output_paths(output_dir, "daily_top20", ("csv", "json")),
            **latest_output_paths(output_dir, "daily_summary", ("md",)),
        }
        archive = archive_output_files(
            output_dir,
            report_type="market_scan",
            analysis_date=report["analysis_date"],
            basenames=["daily_top20", "daily_summary"],
            extensions=("csv", "json", "md"),
        )
    return _bundle(report, output_dir, latest, archive)


def generate_single_stock_committee_report(
    project_root: Path,
    *,
    symbol: str,
    analysis_date: str | None = None,
    style: str | None = None,
    output_root: Path | None = None,
    persist: bool = True,
    ensure_daily_brief: bool = True,
) -> dict[str, Any]:
    (
        settings,
        weights,
        universe,
        action_rules,
        indicator_catalog,
        style_weights,
        strategy_modules,
        evaluation_metrics,
        agent_personas,
    ) = load_single_stock_committee_config(project_root)
    output_dir = resolve_output_dir(output_root or project_root, settings)
    daily_basename = settings.get("daily_market_brief", {}).get("output_basename", "daily_market_brief")
    target_date = analysis_date or date.today().isoformat()

    daily_brief = load_saved_report(
        output_dir,
        basename=daily_basename,
        report_type="daily_taiwan_market_brief",
        analysis_date=target_date,
    )
    daily_bundle: dict[str, Any] | None = None
    if daily_brief is None and ensure_daily_brief:
        daily_bundle = generate_daily_market_brief(
            project_root,
            analysis_date=target_date,
            output_root=output_root,
            persist=True,
        )
        daily_brief = daily_bundle["report"]
    if daily_brief is None:
        raise ValueError("Daily market brief is required before generating a single-stock committee report.")

    basename = settings.get("single_stock_committee", {}).get("output_basename", "single_stock_committee")
    report = _generate_single_stock_committee_core(
        settings,
        weights,
        universe,
        action_rules,
        indicator_catalog,
        style_weights,
        strategy_modules,
        evaluation_metrics,
        agent_personas,
        symbol=symbol,
        analysis_date=target_date,
        style=style,
        daily_brief=daily_brief,
    )

    latest: dict[str, str] = {}
    archive: dict[str, str] = {}
    if persist:
        output_paths = write_single_stock_committee_outputs(output_dir, report, basename=basename)
        latest = output_paths["latest"]
        archive = output_paths["archive"]

    bundle = _bundle(report, output_dir, latest, archive)
    bundle["linked_daily_brief"] = daily_brief
    if daily_bundle is not None:
        bundle["generated_daily_brief"] = daily_bundle
    return bundle


def list_report_history(project_root: Path, *, output_root: Path | None = None, limit: int = 20) -> list[dict[str, Any]]:
    settings, _, _, _ = load_project_config(project_root)
    output_dir = resolve_output_dir(output_root or project_root, settings)
    return list_archive_entries(output_dir, limit=limit)
