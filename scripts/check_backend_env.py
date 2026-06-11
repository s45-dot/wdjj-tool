#!/usr/bin/env python3
import sys

REQUIRED_PACKAGES = ["fastapi", "uvicorn", "pillow", "python-multipart"]

def main():
    missing = []
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)
    else:
        print("OK")
        sys.exit(0)

if __name__ == "__main__":
    main()