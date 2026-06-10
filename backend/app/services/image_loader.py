from pathlib import Path

from PIL import Image


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
