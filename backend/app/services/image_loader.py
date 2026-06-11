import re
from pathlib import Path

from PIL import Image

from ..config import UPLOAD_DIR


def load_and_validate(file_path: Path) -> dict:
    """Open and validate an image file.

    Args:
        file_path: Path to the image file.

    Returns:
        dict with keys 'width' and 'height'.

    Raises:
        ValueError: If the file is not a valid image.
    """
    try:
        img = Image.open(file_path)
        img.verify()  # lightweight verification (doesn't fully decode)
        # After verify() the image is closed; re-open to get dimensions
        img = Image.open(file_path)
        return {"width": img.width, "height": img.height}
    except Exception as exc:
        raise ValueError(f"Invalid image file: {exc}") from exc


def load_image_by_id(imageId: str) -> tuple:
    """Load an image by its ID.

    Args:
        imageId: Image identifier (alphanumeric, underscore, or dash).

    Returns:
        Tuple of (Image object, width, height).

    Raises:
        ValueError: If imageId contains invalid characters.
        FileNotFoundError: If image file doesn't exist.
    """
    if not re.match(r"^[a-zA-Z0-9_-]+$", imageId):
        raise ValueError(f"Invalid imageId: {imageId!r}")

    file_path = UPLOAD_DIR / f"{imageId}.png"
    if not file_path.exists():
        raise FileNotFoundError(f"Image not found: {imageId}")

    img = Image.open(file_path).convert("RGBA")
    return (img, img.width, img.height)
