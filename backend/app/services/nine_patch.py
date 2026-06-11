"""Nine-patch image generation service.

Generates Android-style 9-patch images from source images with configurable
cap insets and content insets.
"""

from PIL import Image


def generate_nine_patch_image(
    source_image: Image.Image,
    cap_insets: dict,
    content_insets: dict,
) -> Image.Image:
    """Generate a nine-patch image from a source image.

    Args:
        source_image: RGBA source image to use as content.
        cap_insets: Dict with keys 'left' and 'right' defining the cap areas.
        content_insets: Dict with keys 'left', 'top', 'right', 'bottom'
            defining the content area.

    Returns:
        New RGBA Image object with the nine-patch border drawn.
    """
    w = source_image.width
    h = source_image.height

    # Output size = (w+2, h+2)
    result = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))

    # Paste source at (1, 1)
    result.paste(source_image, (1, 1))

    black = (0, 0, 0, 255)

    # Top edge: from (1+cap_insets.left, 0) to (w-cap_insets.right, 0)
    top_start_x = 1 + cap_insets["left"]
    top_end_x = w - cap_insets["right"]
    for x in range(top_start_x, top_end_x):
        result.putpixel((x, 0), black)

    # Left edge: from (0, 1+cap_insets.top) to (0, h-cap_insets.bottom)
    left_start_y = 1 + cap_insets["top"]
    left_end_y = h - cap_insets["bottom"]
    for y in range(left_start_y, left_end_y):
        result.putpixel((0, y), black)

    # Bottom edge: from (1+content_insets.left, h+1) to (w-content_insets.right, h+1)
    bottom_start_x = 1 + content_insets["left"]
    bottom_end_x = w - content_insets["right"]
    for x in range(bottom_start_x, bottom_end_x):
        result.putpixel((x, h + 1), black)

    # Right edge: from (w+1, 1+content_insets.top) to (w+1, h-content_insets.bottom)
    right_start_y = 1 + content_insets["top"]
    right_end_y = h - content_insets["bottom"]
    for y in range(right_start_y, right_end_y):
        result.putpixel((w + 1, y), black)

    return result
