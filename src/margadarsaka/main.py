#!/usr/bin/env python3
"""
Margadarsaka AI Career Advisor Main Entry Point
This module provides the main entry point for the UV script
"""

import sys
from pathlib import Path


def main():
    """Main entry point for the margadarsaka UV script"""
    # Add the project root to the Python path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    # Import and run the main launcher
    try:
        from run import main as run_main

        run_main()
    except ImportError as e:
        print(f"❌ Error importing run module: {e}")
        print("💡 Try running from the project root directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
