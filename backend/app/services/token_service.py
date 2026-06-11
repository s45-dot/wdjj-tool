"""Token management – generate, save, and load a secret token."""

import secrets
from pathlib import Path


def generate_token() -> str:
    """Return a random URL-safe token (16 bytes → ~22 chars)."""
    return secrets.token_urlsafe(16)


def save_token(token: str, path: Path) -> None:
    """Write *token* to *path* (creates parent directories if needed)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(token, encoding="utf-8")


def load_token(path: Path) -> str:
    """Read and return the token stored at *path*.

    Raises ``FileNotFoundError`` when the token file does not exist.
    """
    return path.read_text(encoding="utf-8")
