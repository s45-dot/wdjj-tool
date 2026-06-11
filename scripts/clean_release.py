#!/usr/bin/env python3
"""Clean up development artifacts for Bubble Stretch Tool release.

Removes:
  - data/uploads
  - data/exports
  - data/tmp
  - data/logs
  - __pycache__ directories
  - .pytest_cache
  - .DS_Store files
  - node_modules directories
"""

import shutil
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def rmtree(path: Path) -> None:
    """Remove a directory tree if it exists."""
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
        print(f"  🗑️  Removed: {path.relative_to(PROJECT)}")
    elif path.exists():
        print(f"  ⚠️  Not a directory: {path.relative_to(PROJECT)}")


def remove_files(pattern: str) -> None:
    """Remove files matching a pattern recursively."""
    removed = 0
    for f in PROJECT.rglob(pattern):
        if f.is_file() or f.is_symlink():
            f.unlink()
            removed += 1
        elif f.is_dir():
            shutil.rmtree(f)
            removed += 1
    if removed:
        print(f"  🗑️  Removed {removed} items matching {pattern!r}")
    else:
        print(f"  ✓ No items matching {pattern!r}")


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 50)
    print("  Bubble Stretch Tool — Release Cleanup")
    print("=" * 50)
    if dry_run:
        print("  (dry run — no files will be removed)")
    print()

    targets = [
        PROJECT / "data" / "uploads",
        PROJECT / "data" / "exports",
        PROJECT / "data" / "tmp",
        PROJECT / "data" / "logs",
    ]

    for t in targets:
        if dry_run:
            if t.exists():
                print(f"  Would remove: {t.relative_to(PROJECT)}/")
            else:
                print(f"  ✓ {t.relative_to(PROJECT)}/ does not exist")
        else:
            rmtree(t)

    patterns = ["__pycache__", ".pytest_cache", ".DS_Store", "node_modules"]

    for pat in patterns:
        if dry_run:
            matches = list(PROJECT.rglob(pat))
            if matches:
                print(f"  Would remove {len(matches)} items matching {pat!r}")
        else:
            remove_files(pat)

    print()
    if dry_run:
        print("  Dry run complete. Pass no args to actually clean.")
    else:
        print("  ✅ Cleanup complete. Ready for release packaging.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
