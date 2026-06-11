"""Android 9-patch JSON export service."""


def build_android_json(
    asset_name: str,
    image_width: int,
    image_height: int,
    scale: int,
    cap_insets: dict,
    content_insets: dict,
) -> dict:
    """Build Android 9-patch JSON representation.
    
    Args:
        asset_name: Name of the asset file.
        image_width: Width of the source image in pixels.
        image_height: Height of the source image in pixels.
        scale: Image scale factor (e.g., 1, 2, 3).
        cap_insets: Dict with keys 'top', 'right', 'bottom', 'left'.
        content_insets: Dict with keys 'top', 'right', 'bottom', 'left'.
    
    Returns:
        Dict containing the Android 9-patch configuration.
    """
    return {
        "assetName": asset_name,
        "widthPx": image_width,
        "heightPx": image_height,
        "scale": scale,
        "stretchX": {
            "from": cap_insets["left"],
            "to": image_width - cap_insets["right"] - 1,
        },
        "stretchY": {
            "from": cap_insets["top"],
            "to": image_height - cap_insets["bottom"] - 1,
        },
        "padding": {
            "left": content_insets["left"],
            "right": content_insets["right"],
            "top": content_insets["top"],
            "bottom": content_insets["bottom"],
        },
    }
