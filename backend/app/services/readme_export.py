"""README markdown export service."""


def build_readme(
    asset_name: str,
    image_width: int,
    image_height: int,
    scale: int,
    cap_insets: dict,
    content_insets: dict,
) -> str:
    """Build README markdown for a 9-patch asset.
    
    Args:
        asset_name: Name of the asset file.
        image_width: Width of the source image in pixels.
        image_height: Height of the source image in pixels.
        scale: Scale factor (e.g., 1 for 1x, 2 for 2x/retina).
        cap_insets: Dict with keys 'top', 'right', 'bottom', 'left' in pixels.
        content_insets: Dict with keys 'top', 'right', 'bottom', 'left' in pixels.
    
    Returns:
        Markdown string with complete 9-patch documentation.
    """
    # Convert px to pt (points)
    def px_to_pt(px: int) -> float:
        return round(px / scale, 2)

    # Android section
    android_section = (
        f"## Android\n\n"
        f"- **stretchX**: {cap_insets['left']} → {image_width - cap_insets['right'] - 1}\n"
        f"- **stretchY**: {cap_insets['top']} → {image_height - cap_insets['bottom'] - 1}\n"
        f"- **padding**: L{content_insets['left']} R{content_insets['right']} T{content_insets['top']} B{content_insets['bottom']}\n"
    )

    # iOS Swift example
    ios_section = (
        f"## iOS (Swift)\n\n"
        f"```swift\n"
        f"let image = UIImage(named: \"{asset_name}\")\n"
        f"let stretchableImage = image?.resizableImage(\n"
        f"    withCapInsets: UIEdgeInsets(\n"
        f"        top: {px_to_pt(cap_insets['top'])},\n"
        f"        left: {px_to_pt(cap_insets['left'])},\n"
        f"        bottom: {px_to_pt(cap_insets['bottom'])},\n"
        f"        right: {px_to_pt(cap_insets['right'])}\n"
        f"    ),\n"
        f"    resizingMode: .stretch\n"
        f")\n"
        f"```\n"
    )

    # Helper for pt formatting
    def fmt_pt(v: int) -> str:
        return f"{px_to_pt(v)}pt"

    # Cap insets pt values
    cap_pt = {
        "t": fmt_pt(cap_insets["top"]),
        "r": fmt_pt(cap_insets["right"]),
        "b": fmt_pt(cap_insets["bottom"]),
        "l": fmt_pt(cap_insets["left"]),
    }
    content_pt = {
        "t": fmt_pt(content_insets["top"]),
        "r": fmt_pt(content_insets["right"]),
        "b": fmt_pt(content_insets["bottom"]),
        "l": fmt_pt(content_insets["left"]),
    }

    # Notes section
    notes_section = (
        f"## Measurements\n\n"
        f"- **Scale**: {scale}x\n"
        f"- **Image size**: {image_width}×{image_height}px\n"
        f"- **Cap insets (px)**: L{cap_insets['left']} R{cap_insets['right']} T{cap_insets['top']} B{cap_insets['bottom']}px\n"
        f"- **Cap insets (pt)**: L{cap_pt['l']} R{cap_pt['r']} T{cap_pt['t']} B{cap_pt['b']}\n"
        f"- **Content insets (px)**: L{content_insets['left']} R{content_insets['right']} T{content_insets['top']} B{content_insets['bottom']}px\n"
        f"- **Content insets (pt)**: L{content_pt['l']} R{content_pt['r']} T{content_pt['t']} B{content_pt['b']}\n"
    )

    # Combine all sections
    readme = (
        f"# {asset_name}\n\n"
        f"## Image Dimensions\n\n"
        f"- Width: {image_width}px\n"
        f"- Height: {image_height}px\n\n"
        f"{android_section}"
        f"{ios_section}"
        f"{notes_section}"
    )

    return readme
