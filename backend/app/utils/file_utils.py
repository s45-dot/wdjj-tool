from pathlib import Path


def safe_join_path(base: Path, *parts: str) -> Path:
    """Safely join path components, preventing directory traversal.

    Args:
        base: Base path to join from.
        *parts: Path components to append.

    Returns:
        Joined path object.

    Raises:
        ValueError: If any component contains '..' or '/'.
    """
    for part in parts:
        if ".." in part or "/" in part:
            raise ValueError(f"Invalid path component: {part!r}")
    return base.joinpath(*parts)


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist.

    Args:
        path: Directory path to ensure exists.

    Returns:
        The path object (unchanged).
    """
    path.mkdir(parents=True, exist_ok=True)
    return path