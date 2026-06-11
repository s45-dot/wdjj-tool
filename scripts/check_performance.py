#!/usr/bin/env python3
"""Performance measurement script for Bubble Stretch Tool.

Measures:
  - Single export time
  - Batch 10 export time
  - Prints summary

Requirements:
  - Backend server must be running on localhost:8080
  - A test image must be uploaded first
"""

import sys
import time
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8080"

# Path to a test image (the script's own directory)
SCRIPT_DIR = Path(__file__).resolve().parent
TEST_IMAGE = SCRIPT_DIR.parent / "demos" / "android" / "bubble_left.9.png"


def ensure_uploaded() -> str | None:
    """Upload the test image and return its imageId, or None on failure."""
    if not TEST_IMAGE.exists():
        print(f"⚠️  Test image not found: {TEST_IMAGE}")
        print("   Uploading available PNG from current dir...")

        # Try to find any PNG in the workspace
        pngs = list(SCRIPT_DIR.parent.rglob("*.png"))
        test_img = next((p for p in pngs if "token" not in p.name.lower()), None)
        if not test_img:
            print("❌ No PNG test image found. Cannot run performance tests.")
            return None
    else:
        test_img = TEST_IMAGE

    print(f"📤 Uploading {test_img.name}...")
    try:
        with open(test_img, "rb") as f:
            resp = requests.post(
                f"{BASE_URL}/api/upload",
                files={"file": (test_img.name, f, "image/png")},
                timeout=30,
            )
        resp.raise_for_status()
        data = resp.json()
        print(f"   Uploaded: {data['imageId']} ({data['width']}×{data['height']})")
        return data["imageId"]
    except requests.RequestException as exc:
        print(f"❌ Upload failed: {exc}")
        return None


def measure_single_export(image_id: str) -> float | None:
    """Measure time for a single export.

    Returns elapsed seconds, or None on failure.
    """
    print("   Exporting single image...")
    payload = {
        "imageId": image_id,
        "scale": 1,
        "capInsets": {"top": 20, "right": 20, "bottom": 20, "left": 20},
        "contentInsets": {"top": 10, "right": 10, "bottom": 10, "left": 10},
        "preview": {"targetWidth": 240, "targetHeight": 80},
        "outputs": {
            "androidNinePatch": True,
            "iosJson": True,
            "androidJson": True,
            "previewPng": True,
            "readme": True,
            "sourcePng": True,
        },
    }

    try:
        start = time.perf_counter()
        resp = requests.post(
            f"{BASE_URL}/api/export",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        elapsed = time.perf_counter() - start
        resp.raise_for_status()
        print(f"   ✅ Single export: {elapsed:.3f}s")
        return elapsed
    except requests.RequestException as exc:
        print(f"   ❌ Single export failed: {exc}")
        return None


def measure_batch_10_export(image_id: str) -> float | None:
    """Measure time for batch-exporting 10 copies of the same image.

    Returns elapsed seconds, or None on failure.
    """
    images = [{"imageId": image_id} for _ in range(10)]
    payload = {
        "images": images,
        "capInsets": {"top": 20, "right": 20, "bottom": 20, "left": 20},
        "contentInsets": {"top": 10, "right": 10, "bottom": 10, "left": 10},
        "selectedScales": [1],
    }

    print("   Batch exporting 10 images...")
    try:
        start = time.perf_counter()
        resp = requests.post(
            f"{BASE_URL}/api/export/batch",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120,
        )
        elapsed = time.perf_counter() - start
        resp.raise_for_status()
        print(f"   ✅ Batch 10 export: {elapsed:.3f}s")
        return elapsed
    except requests.RequestException as exc:
        print(f"   ❌ Batch export failed: {exc}")
        return None


def main():
    print("=" * 50)
    print("  Bubble Stretch Tool — Performance Check")
    print("=" * 50)

    # Check server connectivity
    print("\n📡 Checking server...")
    try:
        resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
        resp.raise_for_status()
        health = resp.json()
        print(f"   Server OK (version {health.get('version', '?')})")
    except requests.RequestException as exc:
        print(f"❌ Server not reachable at {BASE_URL}: {exc}")
        print("   Start the backend with: scripts/start_backend.py")
        sys.exit(1)

    # Upload test image
    print("\n📤 Uploading test image...")
    image_id = ensure_uploaded()
    if not image_id:
        sys.exit(1)

    # Run measurements
    print("\n⏱️  Measuring export times...")
    single = measure_single_export(image_id)
    batch = measure_batch_10_export(image_id)

    # Summary
    print("\n" + "=" * 50)
    print("  Performance Summary")
    print("=" * 50)
    if single is not None:
        print(f"  Single export:      {single:.3f}s")
    else:
        print("  Single export:      FAILED")
    if batch is not None:
        print(f"  Batch 10 export:    {batch:.3f}s")
        avg = batch / 10
        print(f"  Per image (batch):  {avg:.3f}s")
    else:
        print("  Batch 10 export:    FAILED")

    sys.exit(0)


if __name__ == "__main__":
    main()
