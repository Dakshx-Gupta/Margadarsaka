#!/usr/bin/env python3
"""
Margadarsaka - Unified CLI launcher
Clean entry point for `uv run margadarsaka` and local development.
Supports launching the modern Streamlit UI and (optional) API server.
"""

from __future__ import annotations

import argparse
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "margadarsaka"


def ensure_path() -> None:
    """Ensure src is on PYTHONPATH for local execution."""
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def run_streamlit(modern: bool = True, port: int | None = None) -> int:
    """Run Streamlit UI.

    Args:
        modern: if True, run `ui_modern.py` else fallback to `ui.py`.
        port: optional port; if None, uses Streamlit default.
    Returns: process return code
    """
    ensure_path()
    ui_file = PACKAGE_ROOT / ("ui_modern.py" if modern else "ui.py")
    if not ui_file.exists():
        print(f"❌ UI file not found: {ui_file}")
        return 1

    cmd = [sys.executable, "-m", "streamlit", "run", str(ui_file)]
    if port:
        cmd += ["--server.port", str(port)]

    print("🚀 Launching Streamlit UI:", "modern" if modern else "classic", "→", ui_file)
    try:
        return subprocess.call(cmd)
    except KeyboardInterrupt:
        return 130


def run_api(port: int = 8000) -> int:
    """Run FastAPI server via uvicorn if available."""
    ensure_path()
    app_path = "src.margadarsaka.api:app"
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        app_path,
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
        "--reload",
    ]
    print("🖥️  Launching API server →", app_path)
    try:
        return subprocess.call(cmd)
    except KeyboardInterrupt:
        return 130


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="margadarsaka", description="Margadarsaka launcher"
    )
    parser.add_argument(
        "command", nargs="?", default="ui", choices=["ui", "api"], help="What to run"
    )
    parser.add_argument(
        "--ui-mode",
        choices=["modern", "classic"],
        default="modern",
        help="UI mode to launch",
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port for Streamlit/UI or API server"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.command == "ui":
        modern = args.ui_mode == "modern"
        return run_streamlit(modern=modern, port=args.port)

    if args.command == "api":
        return run_api(port=args.port or 8000)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
