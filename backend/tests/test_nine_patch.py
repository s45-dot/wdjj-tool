"""Pixel-level tests for generate_nine_patch_image service."""

import pytest
from PIL import Image

from app.services.nine_patch import generate_nine_patch_image


@pytest.fixture
def small_rgb_image():
    """Create a small 50x30 RGB test image with a distinctive pattern."""
    img = Image.new("RGB", (50, 30), color=(255, 0, 0))  # Red base
    # Draw a green pixel at (0, 0) for easy identification
    img.putpixel((0, 0), (0, 255, 0))
    return img.convert("RGBA")


def test_output_size(small_rgb_image):
    """Output size = source_size + 2px each dimension."""
    src_w, src_h = small_rgb_image.size
    result = generate_nine_patch_image(small_rgb_image, {"left": 5, "right": 10, "top": 3, "bottom": 7}, {"left": 6, "right": 12, "top": 4, "bottom": 8})
    assert result.size == (src_w + 2, src_h + 2), f"Expected ({src_w + 2}, {src_h + 2}), got {result.size}"


def test_source_pasted_at_offset_1_1(small_rgb_image):
    """Source pasted at (1,1) - pixel at (1,1) matches source (0,0)."""
    result = generate_nine_patch_image(small_rgb_image, {"left": 5, "right": 10, "top": 3, "bottom": 7}, {"left": 6, "right": 12, "top": 4, "bottom": 8})
    assert result.getpixel((1, 1)) == small_rgb_image.getpixel((0, 0))


def test_corner_transparency_4_positions(small_rgb_image):
    """Corners (0,0), (w+1,0), (0,h+1), (w+1,h+1) are all transparent."""
    cap_insets = {"left": 5, "right": 10, "top": 3, "bottom": 7}
    content_insets = {"left": 6, "right": 12, "top": 4, "bottom": 8}
    result = generate_nine_patch_image(small_rgb_image, cap_insets, content_insets)
    w, h = result.size
    assert result.getpixel((0, 0)) == (0, 0, 0, 0), f"Top-left (0,0) not transparent"
    assert result.getpixel((w - 1, 0)) == (0, 0, 0, 0), f"Top-right ({w-1},0) not transparent"
    assert result.getpixel((0, h - 1)) == (0, 0, 0, 0), f"Bottom-left (0,{h-1}) not transparent"
    assert result.getpixel((w - 1, h - 1)) == (0, 0, 0, 0), f"Bottom-right ({w-1},{h-1}) not transparent"


def test_top_edge_black_line(small_rgb_image):
    """Top edge black line at correct stretch coords."""
    cap_insets = {"left": 5, "right": 10}
    result = generate_nine_patch_image(small_rgb_image, cap_insets, {})
    w = small_rgb_image.width
    # Black line from (1+5, 0) to (w-10, 0)
    top_start_x = 1 + cap_insets["left"]
    top_end_x = w - cap_insets["right"]
    for x in range(top_start_x, top_end_x):
        assert result.getpixel((x, 0)) == (0, 0, 0, 255)


def test_left_edge_black_line(small_rgb_image):
    """Left edge black line at correct stretch coords."""
    cap_insets = {"top": 3, "bottom": 7}
    result = generate_nine_patch_image(small_rgb_image, cap_insets, {})
    h = small_rgb_image.height
    # Black line from (0, 1+3) to (0, h-7)
    left_start_y = 1 + cap_insets["top"]
    left_end_y = h - cap_insets["bottom"]
    for y in range(left_start_y, left_end_y):
        assert result.getpixel((0, y)) == (0, 0, 0, 255)


def test_bottom_edge_black_line(small_rgb_image):
    """Bottom edge black line at correct content coords."""
    content_insets = {"left": 6, "right": 12}
    result = generate_nine_patch_image(small_rgb_image, {}, content_insets)
    w = small_rgb_image.width
    h = small_rgb_image.height
    # Black line from (1+6, h+1) to (w-12, h+1)
    bottom_start_x = 1 + content_insets["left"]
    bottom_end_x = w - content_insets["right"]
    for x in range(bottom_start_x, bottom_end_x):
        assert result.getpixel((x, h + 1)) == (0, 0, 0, 255)


def test_right_edge_black_line(small_rgb_image):
    """Right edge black line at correct content coords."""
    content_insets = {"top": 4, "bottom": 8}
    result = generate_nine_patch_image(small_rgb_image, {}, content_insets)
    w = small_rgb_image.width
    h = small_rgb_image.height
    # Black line from (w+1, 1+4) to (w+1, h-8)
    right_start_y = 1 + content_insets["top"]
    right_end_y = h - content_insets["bottom"]
    for y in range(right_start_y, right_end_y):
        assert result.getpixel((w + 1, y)) == (0, 0, 0, 255)


def test_invalid_insets_raise_exception():
    """Invalid insets raise exception."""
    src = Image.new("RGBA", (10, 10), (255, 255, 255, 255))

    # Missing key in cap_insets
    with pytest.raises(KeyError):
        generate_nine_patch_image(src, {}, {})

    # Invalid type (not dict)
    with pytest.raises(TypeError):
        generate_nine_patch_image(src, [], {})

    # Negative values
    with pytest.raises(ValueError):
        generate_nine_patch_image(src, {"left": -1, "right": 0}, {})
