#!/usr/bin/env python3
"""
Run Margadarsaka application using uv
"""
import streamlit.web.cli as stcli
import sys
import subprocess
from pathlib import Path

def main():
    """Main entry point for the application"""
    # Get the directory where this script is located
    app_dir = Path(__file__).parent
    app_file = app_dir / "margadarsaka" / "ui_modern.py"
    
    # Check if we're in a uv environment, if not, use uv run
    if "UV_PROJECT_ENVIRONMENT" in os.environ or "VIRTUAL_ENV" in os.environ:
        # We're already in a virtual environment, run directly
        sys.argv = [
            "streamlit",
            "run",
            str(app_file),
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ]
        sys.exit(stcli.main())
    else:
        # Use uv run to execute in the project environment
        cmd = [
            "uv", "run", "streamlit", "run", str(app_file),
            "--server.port=8501", "--server.address=0.0.0.0"
        ]
        sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    import os
    main()
