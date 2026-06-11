"""Tests for ZIP export service."""

import zipfile
import tempfile
from pathlib import Path

import pytest

from app.services.zip_exporter import create_export_zip, ALLOWED_PATHS


class TestZipExporter:
    """Test cases for create_export_zip function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.all_files = {
            "android/bubble.9.png": b"fake_png_data_android",
            "android/android_nine_patch.json": b'{"capInsets": {}}',
            "ios/ios_cap_insets.json": b'{"capInsets": {}}',
            "preview/bubble_preview.png": b"fake_png_data_preview",
            "source/bubble_original.png": b"fake_png_data_source",
            "README.md": b"# Bubble Stretch Export",
        }

    def test_zip_contains_exactly_six_files(self):
        """Verify ZIP contains exactly 6 files."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            file_count = len(zf.namelist())
            assert file_count == 6, f"Expected 6 files, got {file_count}"

    def test_zip_contains_correct_file_names(self):
        """Verify ZIP contains all expected files."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = set(zf.namelist())
            expected = set(self.all_files.keys())
            assert namelist == expected, f"Expected {expected}, got {namelist}"

    def test_zip_contains_all_allowed_paths(self):
        """Verify all files in ZIP are from ALLOWED_PATHS."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                assert name in ALLOWED_PATHS, f"File {name} not in allowed paths"

    def test_zip_no_absolute_paths(self):
        """Verify ZIP entries have no absolute paths."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                assert not Path(name).is_absolute(), f"Found absolute path: {name}"

    def test_zip_no_parent_directory_references(self):
        """Verify ZIP entries contain no '..' path traversal."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                assert ".." not in name, f"Found '..' in path: {name}"

    def test_zip_no_empty_files(self):
        """Verify ZIP contains no empty files."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                info = zf.getinfo(name)
                assert info.file_size > 0, f"File {name} is empty"

    def test_zip_file_contents_correct(self):
        """Verify ZIP files contain correct content."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for name, content in self.all_files.items():
                assert zf.read(name) == content, f"Content mismatch for {name}"

    def test_invalid_path_rejected(self):
        """Verify non-whitelisted paths raise ValueError."""
        invalid_files = {
            "evil/../../../etc/passwd": b"malicious",
        }

        with pytest.raises(ValueError, match="not allowed"):
            create_export_zip(self.temp_dir, invalid_files)

    def test_partial_files_accepted(self):
        """Verify subset of files can be exported."""
        partial_files = {
            "README.md": b"# Bubble Stretch Export",
            "preview/bubble_preview.png": b"preview_data",
        }
        zip_path = create_export_zip(self.temp_dir, partial_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            assert len(zf.namelist()) == 2

    def test_zip_file_has_correct_mode(self):
        """Verify ZIP is created with ZIP_DEFLATED compression."""
        zip_path = create_export_zip(self.temp_dir, self.all_files)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                assert info.compress_type == zipfile.ZIP_DEFLATED