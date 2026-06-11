"""Tests for preview renderer service."""

import pytest
from PIL import Image

from backend.app.services.preview_renderer import render_nine_slice_preview


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
