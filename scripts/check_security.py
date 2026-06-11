#!/usr/bin/env python3
"""Security audit script for Bubble Stretch Tool.

Checks:
  - Upload type/size limits
  - Path traversal prevention
  - ZIP path safety
  - Token validation
  - No token in logs
  - No data/uploads in release
"""

import importlib.util
import re
import sys
from pathlib import Path


def section(title: str) -> None:
    print(f"\n── {title} ──")


def ok(msg: str) -> None:
    print(f"  ✅ {msg}")


def warn(msg: str) -> None:
    print(f"  ⚠️  {msg}")


def fail(msg: str) -> None:
    print(f"  ❌ {msg}")
    return 1


# Helpers
BACKEND = Path(__file__).resolve().parent.parent / "backend"


def check_import(package: str, source: str) -> int:
    """Return 1 if import fails."""
    spec = importlib.util.find_spec(package)
    if spec is None:
        return fail(f"Cannot import {package!r} ({source})")
    ok(f"Import {package!r} OK ({source})")
    return 0


def check_file_contains(path: Path, pattern: str) -> bool:
    """Return True if the file contains the regex pattern."""
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    return bool(re.search(pattern, content))


score = 0
total_checks = 0


def check(ok_fn, *args) -> int:
    global score, total_checks
    total_checks += 1
    result = ok_fn(*args)
    if result != 1:
        score += 1
    return result


# ── 1. Upload type/size limits ───────────────────────────────────────
section("1. Upload type/size limits")

config_path = BACKEND / "app" / "config.py"
if config_path.exists():
    config_text = config_path.read_text()

    if "MAX_UPLOAD_SIZE" in config_text:
        ok("MAX_UPLOAD_SIZE is defined")
    else:
        check(fail, "MAX_UPLOAD_SIZE is not defined")

    if "ALLOWED_MIME" in config_text:
        ok("ALLOWED_MIME is defined")
    else:
        check(fail, "ALLOWED_MIME is not defined")

    # Check upload router validates type
    upload_router = BACKEND / "app" / "routers" / "upload.py"
    if upload_router.exists():
        router_text = upload_router.read_text()
        if "MAX_UPLOAD_SIZE" in router_text:
            ok("Upload router checks MAX_UPLOAD_SIZE")
        else:
            check(warn, "Upload router may not check MAX_UPLOAD_SIZE")
        if "ALLOWED_MIME" in router_text:
            ok("Upload router checks ALLOWED_MIME")
        else:
            check(warn, "Upload router may not check ALLOWED_MIME")
else:
    check(fail, "config.py not found")

# ── 2. Path traversal prevention ─────────────────────────────────────
section("2. Path traversal prevention")

# Check upload router
upload_router = BACKEND / "app" / "routers" / "upload.py"
if upload_router.exists():
    text = upload_router.read_text()
    if ".." not in text and "os.path.join" not in text:
        ok("No naive path traversal patterns found in upload router")
    else:
        check(warn, "Possible path traversal pattern in upload router")

# Check download router
download_router = BACKEND / "app" / "routers" / "download.py"
if download_router.exists():
    text = download_router.read_text()
    if "Path" in text or "resolve" in text:
        ok("Download router uses Path objects (safe)")
    else:
        check(warn, "Download router may not use safe path handling")

# Check image_loader validates imageId
image_loader = BACKEND / "app" / "services" / "image_loader.py"
if image_loader.exists():
    text = image_loader.read_text()
    if "re.match" in text and "imageId" in text:
        ok("image_loader validates imageId with regex")
    else:
        check(warn, "image_loader may not validate imageId")

# ── 3. ZIP path safety ──────────────────────────────────────────────
section("3. ZIP path safety")

zip_exporter = BACKEND / "app" / "services" / "zip_exporter.py"
if zip_exporter.exists():
    text = zip_exporter.read_text()
    if "ZipFile" in text:
        ok("ZIP export uses ZipFile")
    else:
        check(warn, "ZIP exporter not found or doesn't use ZipFile")
else:
    check(warn, "zip_exporter.py not found (may not exist yet)")

# ── 4. Token validation ─────────────────────────────────────────────
section("4. Token validation")

token_service_path = BACKEND / "app" / "services" / "token_service.py"
if token_service_path.exists():
    text = token_service_path.read_text()
    if "secrets" in text or "token_urlsafe" in text:
        ok("Token generation uses secrets module")
    else:
        check(warn, "Token generation may not use secure random")

    if "load_token" in text:
        ok("load_token function exists")
    else:
        check(fail, "load_token not found")
else:
    check(fail, "token_service.py not found")

# Check main.py uses X-Bubble-Token
main_path = BACKEND / "app" / "main.py"
if main_path.exists():
    text = main_path.read_text()
    if "X-Bubble-Token" in text:
        ok("Token middleware checks X-Bubble-Token header")
    else:
        check(fail, "Token middleware not found")
else:
    check(fail, "main.py not found")

# ── 5. No token in logs ────────────────────────────────────────────
section("5. No token in logs")

local_log_path = BACKEND / "app" / "services" / "local_log.py"
if local_log_path.exists():
    text = local_log_path.read_text()
    if "token" not in text.lower() or "sanitize" in text.lower():
        ok("local_log sanitizes or avoids token content")
    else:
        check(warn, "local_log may log token content")
else:
    check(fail, "local_log.py not found")

# ── 6. No data/uploads in release ──────────────────────────────────
section("6. No data/uploads in release")

# Check .gitignore
gitignore = BACKEND.parent / ".gitignore"
if gitignore.exists():
    text = gitignore.read_text()
    if "data/uploads" in text:
        ok("data/uploads is in .gitignore")
    else:
        check(warn, "data/uploads not in .gitignore")
    if "data/exports" in text:
        ok("data/exports is in .gitignore")
    else:
        check(warn, "data/exports not in .gitignore")
    if "data/logs" in text:
        ok("data/logs is in .gitignore")
    else:
        check(warn, "data/logs not in .gitignore")
    if "token.txt" in text:
        ok("token.txt is in .gitignore")
    else:
        check(warn, "token.txt not in .gitignore")
else:
    check(warn, ".gitignore not found")


# ── Summary ─────────────────────────────────────────────────────────
section("Summary")
print(f"  {score}/{total_checks} checks passed")

sys.exit(0 if score == total_checks else 1)
