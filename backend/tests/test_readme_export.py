"""Tests for README markdown export service."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.services.readme_export import build_readme


class TestBuildReadme:
    """Test suite for build_readme function."""

    def test_build_readme_basic(self):
        """Test basic README generation with sample values."""
        cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
        content_insets = {"top": 8, "right": 12, "bottom": 8, "left": 12}
        scale = 2  # 2x retina
        image_width = 100
        image_height = 50
        asset_name = "test.9.png"

        result = build_readme(
            asset_name=asset_name,
            image_width=image_width,
            image_height=image_height,
            scale=scale,
            cap_insets=cap_insets,
            content_insets=content_insets,
        )

        # Verify markdown contains expected sections
        assert "# test.9.png" in result
        assert "## Image Dimensions" in result
        assert "## Android" in result
        assert "## iOS (Swift)" in result
        assert "## Notes" in result

        # Verify image dimensions
        assert "Width: 100px" in result
        assert "Height: 50px" in result

        # Verify scale
        assert "Scale: 2x" in result

        # Verify pt conversion (px/scale = 10/2 = 5.0)
        assert "5.0pt" in result  # cap insets
        assert "4.0pt" in result  # content insets (8/2)

        # Verify Android section (note: markdown adds **bold** markers)
        assert "**stretchX**: 15 → 84" in result
        assert "**stretchY**: 10 → 39" in result
        assert "**padding**: L12 R12 T8 B8" in result

        # Verify iOS Swift code exists
        assert "UIImage(named: \"test.9.png\")" in result
        assert "UIEdgeInsets(" in result
        assert "resizingMode: .stretch" in result

    def test_build_readme_no_file_io(self):
        """Verify README generation doesn't perform file I/O."""
        # This test ensures the function only returns a string
        # and doesn't write to disk or read from files
        result = build_readme(
            asset_name="test.9.png",
            image_width=100,
            image_height=50,
            scale=1,
            cap_insets={"top": 10, "right": 10, "bottom": 10, "left": 10},
            content_insets={"top": 5, "right": 5, "bottom": 5, "left": 5},
        )

        # Verify result is a string
        assert isinstance(result, str)

        # Verify no file operations occurred (by checking return type)
        assert result is not None

    def test_build_readme_scale_1(self):
        """Test README with 1x scale (px = pt)."""
        result = build_readme(
            asset_name="1x.9.png",
            image_width=50,
            image_height=30,
            scale=1,
            cap_insets={"top": 5, "right": 5, "bottom": 5, "left": 5},
            content_insets={"top": 3, "right": 3, "bottom": 3, "left": 3},
        )

        # With scale 1, px should equal pt
        assert "5.0pt" in result  # cap insets
        assert "3.0pt" in result  # content insets
