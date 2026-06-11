#!/usr/bin/env python3
"""Release package verification for Bubble Stretch Tool.

Verifies:
  - README.md exists
  - docs/ directory exists (with content)
  - backend/ directory exists
  - frontend/ directory exists
  - No data/uploads
  - No .env files
  - No token files
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

errors = []
warnings = []


def check(msg: str, cond: bool, is_error: bool = True) -> None:
    if cond:
        print(f"  ✅ {msg}")
    elif is_error:
        print(f"  ❌ {msg}")
        errors.append(msg)
    else:
        print(f"  ⚠️  {msg}")
        warnings.append(msg)


def main():
    print("=" * 50)
    print("  Bubble Stretch Tool — Release Package Check")
    print("=" * 50)
    print()

    # ── Required files/dirs ──
    print("  Required files:")
    check("README.md exists", (PROJECT / "README.md").is_file())
    check("docs/ exists and is a directory", (PROJECT / "docs").is_dir())
    check("backend/ exists and is a directory", (PROJECT / "backend").is_dir())
    check("frontend/ exists and is a directory", (PROJECT / "frontend").is_dir())

    # Check docs/ has content
    docs_path = PROJECT / "docs"
    docs_files = list(docs_path.glob("*")) if docs_path.is_dir() else []
    check("docs/ contains at least one file", len(docs_files) > 0)

    # Check backend has app/
    check("backend/app/ exists", (PROJECT / "backend" / "app").is_dir())
    check("backend/requirements.txt exists", (PROJECT / "backend" / "requirements.txt").is_file())

    # Check frontend has src/
    check("frontend/src/ exists", (PROJECT / "frontend" / "src").is_dir())
    check("frontend/package.json exists", (PROJECT / "frontend" / "package.json").is_file())

    # Check scripts exist
    scripts_path = PROJECT / "scripts"
    required_scripts = [
        "start_backend.py",
        "start_macos.command",
        "start_windows.bat",
        "build_frontend.sh",
    ]
    for script in required_scripts:
        check(f"scripts/{script} exists", (scripts_path / script).exists())

    # ── Things that should NOT be present ──
    print("\n  Security checks (should NOT be present):")
    check("No data/uploads directory", not (PROJECT / "data" / "uploads").is_dir())
    check("No .env files in workspace",
          len(list(PROJECT.rglob(".env"))) == 0)
    check("No token files (token.txt)",
          len(list(PROJECT.rglob("token.txt"))) == 0)
    check("No __pycache__ directories",
          len(list(PROJECT.rglob("__pycache__"))) == 0)

    # ── Summary ──
    print("\n" + "=" * 50)
    total_errors = len(errors)
    total_warnings = len(warnings)
    total_checks = 4 + len(required_scripts) + 4  # required + security
    passed = total_checks - total_errors

    print(f"  Checks: {passed}/{total_checks} passed")
    if total_warnings > 0:
        print(f"  Warnings: {total_warnings}")
    if total_errors > 0:
        print(f"  Errors: {total_errors} — release is NOT ready")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
