"""Tests for preview renderer service."""

import pytest
from PIL import Image

from app.services.preview_renderer import render_nine_slice_preview


def test_render_nine_slice_preview_dimensions():
    """Test preview output dimensions match target."""
    source = Image.new("RGB", (100, 60), color=(255, 0, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
    target = (200, 100)
    
    result = render_nine_slice_preview(source, *target, cap_insets)
    
    assert result.size == target
    assert result.mode == "RGBA"


def test_render_nine_slice_preview_rgba_mode():
    """Test preview output is RGBA mode."""
    source = Image.new("RGB", (100, 60), color=(0, 255, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
    target = (200, 100)
    
    result = render_nine_slice_preview(source, *target, cap_insets)
    
    assert result.mode == "RGBA"


def test_render_nine_slice_preview_alpha_channel():
    """Test preview has proper alpha channel."""
    source = Image.new("RGB", (100, 60), color=(0, 0, 255))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
    target = (200, 100)
    
    result = render_nine_slice_preview(source, *target, cap_insets)
    
    # Check some pixels have alpha values
    pixel = result.getpixel((10, 10))
    assert len(pixel) == 4  # RGBA
    assert pixel[3] > 0  # Not fully transparent


def test_render_nine_slice_preview_empty_insets():
    """Test preview with zero insets (whole image scales)."""
    source = Image.new("RGB", (100, 60), color=(128, 128, 128))
    cap_insets = {"top": 0, "right": 0, "bottom": 0, "left": 0}
    target = (200, 100)

    result = render_nine_slice_preview(source, *target, cap_insets)

    assert result.size == target
    assert result.mode == "RGBA"


def test_render_nine_slice_preview_output_rgba():
    """Test preview output is RGBA mode."""
    source = Image.new("RGB", (100, 60), color=(255, 0, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
    target = (200, 100)

    result = render_nine_slice_preview(source, *target, cap_insets)

    assert result.mode == "RGBA"
    assert result.getbands() == ("R", "G", "B", "A")


def test_render_nine_slice_preview_alpha_channel_preserved():
    """Test preview preserves alpha channel with transparency."""
    source = Image.new("RGBA", (100, 60), color=(255, 0, 0, 128))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
    target = (200, 100)

    result = render_nine_slice_preview(source, *target, cap_insets)

    assert result.mode == "RGBA"
    pixel = result.getpixel((50, 50))
    assert pixel[3] == 128, "Alpha channel should be preserved"


def test_render_nine_slice_preview_transparent_background():
    """Test preview has transparent background (alpha=0)."""
    source = Image.new("RGBA", (100, 60), color=(255, 0, 0, 255))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
    target = (200, 100)

    result = render_nine_slice_preview(source, *target, cap_insets)

    corner_pixel = result.getpixel((0, 0))
    assert corner_pixel[3] == 0, "Corner should be transparent"


def test_render_nine_slice_preview_invalid_targetWidth_zero():
    """Test invalid targetWidth=0 raises error."""
    source = Image.new("RGB", (100, 60), color=(255, 0, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}

    with pytest.raises((ValueError, Exception)):
        render_nine_slice_preview(source, 0, 100, cap_insets)


def test_render_nine_slice_preview_invalid_targetHeight_zero():
    """Test invalid targetHeight=0 raises error."""
    source = Image.new("RGB", (100, 60), color=(255, 0, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}

    with pytest.raises((ValueError, Exception)):
        render_nine_slice_preview(source, 200, 0, cap_insets)


def test_render_nine_slice_preview_invalid_targetWidth_negative():
    """Test invalid targetWidth=-1 raises error."""
    source = Image.new("RGB", (100, 60), color=(255, 0, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}

    with pytest.raises((ValueError, Exception)):
        render_nine_slice_preview(source, -1, 100, cap_insets)


def test_render_nine_slice_preview_invalid_targetHeight_negative():
    """Test invalid targetHeight=-1 raises error."""
    source = Image.new("RGB", (100, 60), color=(255, 0, 0))
    cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}

    with pytest.raises((ValueError, Exception)):
        render_nine_slice_preview(source, 200, -1, cap_insets)
