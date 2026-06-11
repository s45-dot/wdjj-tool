"""Tests for Android JSON export service."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.services.android_export import build_android_json


class TestBuildAndroidJson:
    """Test suite for build_android_json function."""

    def test_build_android_json_basic(self):
        """Test basic JSON generation with sample values."""
        cap_insets = {"top": 10, "right": 15, "bottom": 10, "left": 15}
        content_insets = {"top": 8, "right": 12, "bottom": 8, "left": 12}
        image_width = 100
        image_height = 50
        asset_name = "test.9.png"

        result = build_android_json(
            asset_name=asset_name,
            image_width=image_width,
            image_height=image_height,
            cap_insets=cap_insets,
            content_insets=content_insets,
        )

        # Verify basic fields
        assert result["assetName"] == "test.9.png"
        assert result["widthPx"] == 100
        assert result["heightPx"] == 50

        # Verify stretchX calculations
        # stretchX.from = cap_insets["left"] = 15
        # stretchX.to = image_width - cap_insets["right"] - 1 = 100 - 15 - 1 = 84
        assert result["stretchX"]["from"] == 15
        assert result["stretchX"]["to"] == 84

        # Verify stretchY calculations
        # stretchY.from = cap_insets["top"] = 10
        # stretchY.to = image_height - cap_insets["bottom"] - 1 = 50 - 10 - 1 = 39
        assert result["stretchY"]["from"] == 10
        assert result["stretchY"]["to"] == 39

        # Verify padding (content insets)
        assert result["padding"]["left"] == 12
        assert result["padding"]["right"] == 12
        assert result["padding"]["top"] == 8
        assert result["padding"]["bottom"] == 8

    def test_build_android_json_edge_case_zero(self):
        """Test with zero dimensions and insets."""
        result = build_android_json(
            asset_name="zero.9.png",
            image_width=0,
            image_height=0,
            cap_insets={"top": 0, "right": 0, "bottom": 0, "left": 0},
            content_insets={"top": 0, "right": 0, "bottom": 0, "left": 0},
        )

        assert result["widthPx"] == 0
        assert result["heightPx"] == 0
        assert result["stretchX"]["from"] == 0
        assert result["stretchX"]["to"] == -1  # 0 - 0 - 1
        assert result["stretchY"]["from"] == 0
        assert result["stretchY"]["to"] == -1  # 0 - 0 - 1

    def test_build_android_json_single_pixel(self):
        """Test with single pixel image."""
        result = build_android_json(
            asset_name="single.9.png",
            image_width=1,
            image_height=1,
            cap_insets={"top": 0, "right": 0, "bottom": 0, "left": 0},
            content_insets={"top": 0, "right": 0, "bottom": 0, "left": 0},
        )

        assert result["widthPx"] == 1
        assert result["heightPx"] == 1
        assert result["stretchX"]["from"] == 0
        assert result["stretchX"]["to"] == 0  # 1 - 0 - 1
        assert result["stretchY"]["from"] == 0
        assert result["stretchY"]["to"] == 0  # 1 - 0 - 1
