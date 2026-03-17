"""Windows desktop launcher with file logging for Taiwan Stock Radar."""

from __future__ import annotations

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _log_path() -> Path:
    log_dir = _repo_root() / "output" / "desktop_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "launcher.log"


def _show_error_dialog(message: str) -> None:
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, "Taiwan Stock Radar", 0x10)
    except Exception:
        pass


def main() -> int:
    repo_root = _repo_root()
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    log_path = _log_path()
    with log_path.open("a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"\n=== Taiwan Stock Radar launcher start {timestamp} ===\n")
        log_file.write(f"cwd={os.getcwd()}\n")
        log_file.write(f"repo_root={repo_root}\n")
        log_file.flush()

        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = log_file
        sys.stderr = log_file

        try:
            from main import main as app_main

            return int(app_main())
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 0
            log_file.write(f"SystemExit code={code}\n")
            log_file.flush()
            return code
        except Exception:
            traceback.print_exc(file=log_file)
            log_file.flush()
            _show_error_dialog(
                "Taiwan Stock Radar failed to start.\n\n"
                f"Log file:\n{log_path}"
            )
            return 1
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr


if __name__ == "__main__":
    raise SystemExit(main())
