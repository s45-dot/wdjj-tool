"""Tests for iOS export service."""

import unittest
from backend.app.services.ios_export import build_ios_cap_insets_json


class TestIosExport(unittest.TestCase):
    """Test cases for build_ios_cap_insets_json function."""

    def setUp(self):
        """Set up test fixtures."""
        self.asset_name = "test_button"
        self.image_width = 100
        self.image_height = 50
        self.scale = 2
        self.cap_insets = {"left": 10, "top": 10, "right": 20, "bottom": 20}
        self.content_insets = {"left": 30, "top": 15, "right": 30, "bottom": 15}

    def test_returns_dict(self):
        """Verify function returns a dictionary."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )
        self.assertIsInstance(result, dict)

    def test_all_keys_present(self):
        """Verify all required keys are present in the result."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )
        expected_keys = [
            "assetName",
            "widthPx",
            "heightPx",
            "scale",
            "capInsetsPx",
            "capInsetsPt",
            "contentInsetsPx",
            "contentInsetsPt",
            "swiftExample",
        ]
        for key in expected_keys:
            self.assertIn(key, result, f"Missing required key: {key}")

    def test_pt_values_divided_by_scale(self):
        """Verify pt values are correctly calculated by dividing px by scale."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )

        # Check cap insets pt values
        for key in self.cap_insets:
            expected_pt = self.cap_insets[key] / self.scale
            actual_pt = result["capInsetsPt"][key]
            self.assertEqual(
                actual_pt,
                expected_pt,
                f"capInsetsPt[{key}] should be {expected_pt}, got {actual_pt}",
            )

        # Check content insets pt values
        for key in self.content_insets:
            expected_pt = self.content_insets[key] / self.scale
            actual_pt = result["contentInsetsPt"][key]
            self.assertEqual(
                actual_pt,
                expected_pt,
                f"contentInsetsPt[{key}] should be {expected_pt}, got {actual_pt}",
            )

    def test_pixel_values_unchanged(self):
        """Verify pixel values in the result match the input."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )

        # Check pixel values are unchanged
        for key in self.cap_insets:
            self.assertEqual(result["capInsetsPx"][key], self.cap_insets[key])

        for key in self.content_insets:
            self.assertEqual(result["contentInsetsPx"][key], self.content_insets[key])

    def test_swift_example_contains_correct_values(self):
        """Verify swiftExample contains the correct point values."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )

        swift_code = result["swiftExample"]

        # Check that the Swift code contains the correct point values
        for key, px_value in self.cap_insets.items():
            expected_pt = px_value / self.scale
            self.assertIn(
                f"{expected_pt}",
                swift_code,
                f"swiftExample should contain capInsetsPt[{key}] = {expected_pt}",
            )

        for key, px_value in self.content_insets.items():
            expected_pt = px_value / self.scale
            self.assertIn(
                f"{expected_pt}",
                swift_code,
                f"swiftExample should contain contentInsetsPt[{key}] = {expected_pt}",
            )

    def test_swift_example_contains_asset_name(self):
        """Verify swiftExample contains the asset name."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )

        self.assertIn(
            self.asset_name,
            result["swiftExample"],
            "swiftExample should contain the asset name",
        )

    def test_dimensions_correct(self):
        """Verify image dimensions are correctly stored."""
        result = build_ios_cap_insets_json(
            self.asset_name,
            self.image_width,
            self.image_height,
            self.scale,
            self.cap_insets,
            self.content_insets,
        )

        self.assertEqual(result["widthPx"], self.image_width)
        self.assertEqual(result["heightPx"], self.image_height)
        self.assertEqual(result["scale"], self.scale)
        self.assertEqual(result["assetName"], self.asset_name)


if __name__ == "__main__":
    unittest.main()
