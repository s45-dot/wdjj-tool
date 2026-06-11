"""Nine-slice preview renderer for bubble stretch tool."""

from PIL import Image


def render_nine_slice_preview(
    source_image: Image.Image,
    target_width: int,
    target_height: int,
    cap_insets: dict,
) -> Image.Image:
    """Render a nine-slice preview of the source image.
    
    Algorithm:
    - Split source into 3x3 grid using cap insets
    - Map each region to target dimensions
    - Composite regions in correct positions
    
    Args:
        source_image: PIL Image to render
        target_width: Width of preview output
        target_height: Height of preview output
        cap_insets: Dict with keys top, right, bottom, left
        
    Returns:
        RGBA PIL Image
    """
    src_w, src_h = source_image.size
    src_image = source_image.convert("RGBA")
    
    left = cap_insets.get("left", 0)
    top = cap_insets.get("top", 0)
    right = cap_insets.get("right", 0)
    bottom = cap_insets.get("bottom", 0)
    
    # Source regions
    sx = [0, left, src_w - right, src_w]
    sy = [0, top, src_h - bottom, src_h]
    
    # Destination regions
    dx = [0, left, target_width - right, target_width]
    dy = [0, top, target_height - bottom, target_height]
    
    # Create output image
    result = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
    
    # Composite 3x3 grid
    for row in range(3):
        for col in range(3):
            src_w_region = sx[col + 1] - sx[col]
            src_h_region = sy[row + 1] - sy[row]
            dst_w_region = dx[col + 1] - dx[col]
            dst_h_region = dy[row + 1] - dy[row]
            
            # Crop and resize region
            region = src_image.crop((sx[col], sy[row], sx[col + 1], sy[row + 1]))
            if dst_w_region > 0 and dst_h_region > 0:
                region = region.resize((dst_w_region, dst_h_region), Image.LANCZOS)
                result.paste(region, (dx[col], dy[row]))
    
    return result
