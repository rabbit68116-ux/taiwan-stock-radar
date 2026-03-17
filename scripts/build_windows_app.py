#!/usr/bin/env python3
"""Build the PySide6 desktop app into a PyInstaller one-folder bundle."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    if os.name != "nt":
        print("Windows EXE packaging must be run on a Windows host. The PySide6 desktop app is ready, but this machine cannot emit a Windows executable.")
        return 0

    entry = project_root / "apps" / "windows" / "main.py"
    dist_dir = project_root / "dist" / "windows"
    build_dir = project_root / "build" / "windows"
    sep = ";" if os.name == "nt" else ":"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--windowed",
        "--name",
        "TaiwanStockRadar",
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(build_dir),
        "--specpath",
        str(build_dir),
        "--paths",
        str(project_root / "src"),
        "--add-data",
        f"{project_root / 'config'}{sep}config",
        str(entry),
    ]

    print("Running:", " ".join(cmd))
    env = os.environ.copy()
    env.setdefault("COPYFILE_DISABLE", "1")
    completed = subprocess.run(cmd, cwd=project_root, env=env)
    if completed.returncode != 0:
        return completed.returncode

    bundle_path = dist_dir / "TaiwanStockRadar"
    print(f"Build completed: {bundle_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
