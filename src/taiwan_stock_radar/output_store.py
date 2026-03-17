"""Helpers for latest outputs and archived report history."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


def latest_output_paths(output_dir: Path, basename: str, extensions: tuple[str, ...]) -> dict[str, str]:
    return {
        extension: str(output_dir / f"{basename}.{extension}")
        for extension in extensions
        if (output_dir / f"{basename}.{extension}").exists()
    }


def archive_directory(
    output_dir: Path,
    report_type: str,
    analysis_date: str,
    *,
    symbol: str | None = None,
) -> Path:
    archive_dir = output_dir / "archive" / report_type / analysis_date
    if symbol:
        archive_dir = archive_dir / symbol
    archive_dir.mkdir(parents=True, exist_ok=True)
    return archive_dir


def archive_path(
    output_dir: Path,
    report_type: str,
    analysis_date: str,
    *,
    symbol: str | None = None,
) -> Path:
    path = output_dir / "archive" / report_type / analysis_date
    if symbol:
        path = path / symbol
    return path


def archive_output_files(
    output_dir: Path,
    *,
    report_type: str,
    analysis_date: str,
    basenames: list[str],
    extensions: tuple[str, ...],
    symbol: str | None = None,
) -> dict[str, str]:
    archive_dir = archive_directory(output_dir, report_type, analysis_date, symbol=symbol)
    archived: dict[str, str] = {}
    for basename in basenames:
        for extension in extensions:
            source = output_dir / f"{basename}.{extension}"
            if not source.exists():
                continue
            target = archive_dir / f"{basename}.{extension}"
            shutil.copy2(source, target)
            archived[f"{basename}.{extension}"] = str(target)
    return archived


def write_report_bundle(
    output_dir: Path,
    *,
    basename: str,
    report_type: str,
    analysis_date: str,
    payload: dict[str, Any],
    markdown: str,
    symbol: str | None = None,
) -> dict[str, dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    latest_json = output_dir / f"{basename}.json"
    latest_md = output_dir / f"{basename}.md"
    latest_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    archive_dir = archive_directory(output_dir, report_type, analysis_date, symbol=symbol)
    archive_json = archive_dir / f"{basename}.json"
    archive_md = archive_dir / f"{basename}.md"
    archive_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    archive_md.write_text(markdown, encoding="utf-8")

    return {
        "latest": {"json": str(latest_json), "md": str(latest_md)},
        "archive": {"json": str(archive_json), "md": str(archive_md)},
    }


def load_saved_report(
    output_dir: Path,
    *,
    basename: str,
    report_type: str,
    analysis_date: str,
    symbol: str | None = None,
) -> dict[str, Any] | None:
    latest_path = output_dir / f"{basename}.json"
    if latest_path.exists():
        payload = json.loads(latest_path.read_text(encoding="utf-8"))
        if payload.get("analysis_date") == analysis_date and (
            symbol is None or payload.get("symbol") == symbol
        ):
            return payload

    saved_path = archive_path(output_dir, report_type, analysis_date, symbol=symbol) / f"{basename}.json"
    if saved_path.exists():
        return json.loads(saved_path.read_text(encoding="utf-8"))
    return None


def list_archive_entries(output_dir: Path, limit: int = 20) -> list[dict[str, Any]]:
    archive_root = output_dir / "archive"
    if not archive_root.exists():
        return []

    entries: list[dict[str, Any]] = []
    for json_path in archive_root.rglob("*.json"):
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        relative = json_path.relative_to(archive_root)
        parts = relative.parts
        report_type = parts[0] if parts else payload.get("report_type", "unknown")
        analysis_date = payload.get("analysis_date", parts[1] if len(parts) > 1 else "")
        symbol = payload.get("symbol", parts[2] if len(parts) > 3 else None)
        modified_at = datetime.fromtimestamp(json_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        entries.append(
            {
                "report_type": report_type,
                "analysis_date": analysis_date,
                "symbol": symbol,
                "title": payload.get("project", "Taiwan Stock Radar"),
                "path": str(json_path),
                "modified_at": modified_at,
            }
        )

    entries.sort(key=lambda item: (item["analysis_date"], item["modified_at"]), reverse=True)
    return entries[:limit]
