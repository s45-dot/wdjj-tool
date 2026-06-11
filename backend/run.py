#!/usr/bin/env python3
"""Bootstrap script for Bubble Stretch Tool.

Calls scripts/start_backend.py to start the uvicorn server.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
START_BACKEND_SCRIPT = SCRIPT_DIR / "start_backend.py"


def main():
    args = ["python3", str(START_BACKEND_SCRIPT)] + sys.argv[1:]
    result = subprocess.run(args)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()