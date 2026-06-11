"""Local log service for Bubble Stretch Tool.

Writes daily log files to data/logs/bubble-YYYY-MM-DD.log.
Never logs tokens, never uploads data.
"""

from datetime import date
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "logs"

# Sensitive patterns that should never appear in logs
_SENSITIVE_PATTERNS = [
    "X-Bubble-Token",
    "token.txt",
    "Authorization",
    "Bearer ",
]


def _sanitize(message: str) -> str:
    """Remove or mask sensitive patterns from a log message."""
    sanitized = message
    for pattern in _SENSITIVE_PATTERNS:
        sanitized = sanitized.replace(pattern, "[REDACTED]")
    return sanitized


def write_log(level: str, message: str) -> None:
    """Append a timestamped log entry to the daily log file.

    Args:
        level: Log level string (e.g., INFO, WARNING, ERROR).
        message: Log message content. Will be sanitized.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()  # YYYY-MM-DD
    log_path = LOG_DIR / f"bubble-{today}.log"

    sanitized = _sanitize(message)
    timestamp = date.today().isoformat()  # Runtime timestamp

    line = f"[{timestamp}] [{level}] {sanitized}\n"

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as exc:
        # If we can't write the log, silently fall back — don't crash
        print(f"⚠️  Failed to write log: {exc}")


def read_recent_logs(days: int = 3) -> list[dict]:
    """Read recent log entries across the last N daily log files.

    Args:
        days: Number of past days to scan (default: 3).

    Returns:
        List of dicts with 'date', 'file', and 'line_count'.
        Does NOT return the actual log content (no image data, no tokens).
    """
    from datetime import timedelta

    results: list[dict] = []
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)
        log_path = LOG_DIR / f"bubble-{day.isoformat()}.log"

        if log_path.exists():
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                results.append({
                    "date": day.isoformat(),
                    "file": log_path.name,
                    "line_count": len(lines),
                })
            except OSError:
                continue

    return results
