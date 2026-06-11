#!/usr/bin/env python3
"""Diagnostic report for Bubble Stretch Tool.

Prints:
  - Tool version (from backend/app/version.py)
  - Python version
  - Node.js version
  - OS info
  - Port check (8080)
  - Dependency check (Python packages)
  - Recent log summary (no user images, no token)
"""

import importlib.metadata
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def get_version() -> str:
    """Read version from backend/app/version.py."""
    version_file = PROJECT / "backend" / "app" / "version.py"
    if version_file.exists():
        try:
            ns: dict = {}
            exec(version_file.read_text(), ns)
            return ns.get("VERSION", "unknown")
        except Exception:
            return "unknown (parse error)"
    return "not found"


def run(cmd: list[str], label: str) -> str:
    """Run a command and return its stdout, or an error message."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout.strip()
        return output if output else result.stderr.strip() or "(no output)"
    except FileNotFoundError:
        return "(not installed)"
    except subprocess.TimeoutExpired:
        return "(timed out)"
    except Exception as exc:
        return f"(error: {exc})"


def check_port(port: int = 8080) -> str:
    """Check if a TCP port is in use."""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        return "in use" if result == 0 else "available"
    except Exception as exc:
        return f"(error: {exc})"


def check_python_deps() -> list[tuple[str, str]]:
    """Check key Python dependencies.

    Returns list of (package, status) tuples.
    """
    required = [
        "fastapi",
        "uvicorn",
        "pillow",
        "pydantic",
        "requests",
        "aiofiles",
    ]
    results: list[tuple[str, str]] = []
    for pkg in required:
        try:
            version = importlib.metadata.version(pkg)
            results.append((pkg, version))
        except importlib.metadata.PackageNotFoundError:
            results.append((pkg, "NOT INSTALLED"))
    return results


def recent_log_summary() -> str:
    """Get a summary of recent log files (no content, just counts)."""
    logs_dir = PROJECT / "data" / "logs"
    if not logs_dir.is_dir():
        return "  No log directory found."

    log_files = sorted(logs_dir.glob("bubble-*.log"), reverse=True)[:5]

    if not log_files:
        return "  No log files found."

    lines = []
    total_size = 0
    total_lines = 0
    for lf in log_files:
        try:
            size = lf.stat().st_size
            lc = len(lf.read_text(encoding="utf-8").splitlines())
            total_size += size
            total_lines += lc
            lines.append(f"  {lf.name}: {lc} lines, {size} bytes")
        except OSError:
            lines.append(f"  {lf.name}: (unreadable)")

    summary = f"  {len(log_files)} log file(s), {total_lines} total lines, {total_size} total bytes\n"
    summary += "\n".join(lines)
    return summary


def main():
    print("=" * 55)
    print("  Bubble Stretch Tool — Diagnostic Report")
    print("=" * 55)

    # Version
    print(f"\n  Tool version:    {get_version()}")

    # Environment
    import platform
    print(f"  Python version:  {sys.version.split()[0]}")
    print(f"  Node.js version: {run(['node', '--version'], 'node')}")
    print(f"  OS:              {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  Platform:        {sys.platform}")

    # Port check
    port_status = check_port(8080)
    print(f"  Port 8080:       {port_status}")

    # Dependencies
    print("\n  Python packages:")
    for pkg, ver in check_python_deps():
        status_icon = "✅" if ver != "NOT INSTALLED" else "❌"
        print(f"    {status_icon} {pkg}=={ver}")

    # Frontend deps
    print("\n  Frontend:")
    package_json = PROJECT / "frontend" / "package.json"
    if package_json.exists():
        print(f"    package.json:  present")
    else:
        print(f"    ⚠️  package.json: missing")

    node_modules = PROJECT / "frontend" / "node_modules"
    if node_modules.is_dir():
        print(f"    node_modules:  present")
    else:
        print(f"    node_modules:  missing (run npm install)")

    # Scripts
    print("\n  Scripts:")
    scripts_dir = PROJECT / "scripts"
    if scripts_dir.is_dir():
        scripts = sorted(scripts_dir.glob("*"))
        print(f"    {len(scripts)} script(s) available")
    else:
        print("    scripts/ directory missing")

    # Recent logs (metadata only — no image data, no tokens)
    print("\n  Recent logs:")
    print(recent_log_summary())

    print("\n" + "=" * 55)
    print("  Diagnostic report complete")
    print("=" * 55)

    sys.exit(0)


if __name__ == "__main__":
    main()
