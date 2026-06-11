"""ZIP export service for bubble stretch tool."""

import zipfile
from pathlib import Path
from typing import Dict, Union
import uuid


# Whitelisted file paths for export
ALLOWED_PATHS = frozenset({
    "android/bubble.9.png",
    "android/android_nine_patch.json",
    "ios/ios_cap_insets.json",
    "preview/bubble_preview.png",
    "source/bubble_original.png",
    "README.md",
})

# Multi-scale / batch paths follow the pattern: {image_id}/{scale}x/<rest>
# where <rest> matches one of the allowed paths.  We also accept scale-prefixed
# paths such as "1x/android/bubble.9.png" from the single-image multi-scale
# route.
MULTI_SCALE_ALLOWED = frozenset({
    "android/bubble.9.png",
    "android/android_nine_patch.json",
    "ios/ios_cap_insets.json",
    "preview/bubble_preview.png",
    "source/bubble_original.png",
    "README.md",
})


def create_export_zip(export_dir: Union[str, Path], files: Dict[str, bytes]) -> Path:
    """
    Create a ZIP export file containing the specified assets.

    Args:
        export_dir: Directory where the ZIP file will be created
        files: Dictionary mapping file paths (must be in whitelist) to their binary content

    Returns:
        Path to the created ZIP file

    Raises:
        ValueError: If any file path is not in the whitelist
    """
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    # Validate all file paths against whitelist
    for file_path in files.keys():
        if file_path not in ALLOWED_PATHS:
            raise ValueError(
                f"File path '{file_path}' is not allowed. "
                f"Allowed paths: {sorted(ALLOWED_PATHS)}"
            )

    zip_path = export_dir / "bubble_export.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path, content in files.items():
            zf.writestr(file_path, content)

    return zip_path


def create_multi_scale_export_zip(
    export_dir: Union[str, Path],
    files: Dict[str, bytes],
) -> Path:
    """
    Create a ZIP export file for multi-scale or batch exports.

    This function accepts paths with a more flexible structure:
    - {scale}x/<standard-path>  (e.g. "2x/android/bubble.9.png")
    - {image_id}/{scale}x/<standard-path>  (e.g. "abc123/2x/android/bubble.9.png")

    Args:
        export_dir: Directory where the ZIP file will be created.
        files: Dictionary mapping file paths to their binary content.

    Returns:
        Path to the created ZIP file.
    """
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    zip_path = export_dir / "batch_export.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path, content in files.items():
            zf.writestr(file_path, content)

    return zip_path
