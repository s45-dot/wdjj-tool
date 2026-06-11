"""iOS export service for nine-slice image configuration."""

from typing import Dict, Any


def build_ios_cap_insets_json(
    asset_name: str,
    image_width: int,
    image_height: int,
    scale: int,
    cap_insets: Dict[str, int],
    content_insets: Dict[str, int],
) -> Dict[str, Any]:
    """Build a JSON-serializable dict for iOS cap insets configuration.

    Args:
        asset_name: Name of the asset (e.g., "button_background")
        image_width: Width of the image in pixels
        image_height: Height of the image in pixels
        scale: Image scale factor (e.g., 1, 2, 3)
        cap_insets: Dictionary with cap insets in pixels:
            {"left": int, "top": int, "right": int, "bottom": int}
        content_insets: Dictionary with content insets in pixels:
            {"left": int, "top": int, "right": int, "bottom": int}

    Returns:
        Dictionary with iOS-specific configuration including pixel and point values
    """
    # Calculate point values by dividing pixel values by scale
    cap_insets_pt = {k: v / scale for k, v in cap_insets.items()}
    content_insets_pt = {k: v / scale for k, v in content_insets.items()}

    # Build Swift example code snippet
    swift_example = (
        f'// Asset: {asset_name}\n'
        f'let capInsets = UIEdgeInsets(top: {cap_insets_pt["top"]}, '
        f'left: {cap_insets_pt["left"]}, '
        f'bottom: {cap_insets_pt["bottom"]}, '
        f'right: {cap_insets_pt["right"]})\n'
        f'let contentInsets = UIEdgeInsets(top: {content_insets_pt["top"]}, '
        f'left: {content_insets_pt["left"]}, '
        f'bottom: {content_insets_pt["bottom"]}, '
        f'right: {content_insets_pt["right"]})'
    )

    return {
        "assetName": asset_name,
        "widthPx": image_width,
        "heightPx": image_height,
        "scale": scale,
        "capInsetsPx": cap_insets,
        "capInsetsPt": cap_insets_pt,
        "contentInsetsPx": content_insets,
        "contentInsetsPt": content_insets_pt,
        "swiftExample": swift_example,
    }
