"""Multi-scale export service for Bubble Stretch Tool.

Generates export artifacts for multiple scale factors from a single
source image, reusing existing single-scale export services.
"""

import io
import json
from typing import Dict, List

from PIL import Image

from app.services.android_export import build_android_json
from app.services.ios_export import build_ios_cap_insets_json
from app.services.nine_patch import generate_nine_patch_image
from app.services.preview_renderer import render_nine_slice_preview
from app.services.readme_export import build_readme


def export_multi_scale(
    image_id: str,
    source_image: Image.Image,
    original_bytes: bytes,
    cap_insets: Dict[str, int],
    content_insets: Dict[str, int],
    selected_scales: List[int],
    preview_options: Dict,
    outputs: Dict,
) -> Dict[str, bytes]:
    """Generate export artifacts for multiple selected scales.

    Shared assets (preview PNG, .9.png) are generated once; scale-specific
    metadata (iOS JSON, Android JSON, README) is generated per scale.

    Args:
        image_id: Backend image identifier.
        source_image: PIL Image object loaded from storage.
        original_bytes: Raw PNG bytes of the source image.
        cap_insets: Dict with keys top, right, bottom, left.
        content_insets: Dict with keys top, right, bottom, left.
        selected_scales: List of scale factors (e.g. [1, 2, 3]).
        preview_options: Dict with targetWidth and targetHeight.
        outputs: Dict of boolean output format toggles.

    Returns:
        Dict mapping archive file paths to their byte contents.
        Paths are prefixed with the scale factor, e.g.:
        {
            "1x/android/bubble.9.png": <bytes>,
            "2x/ios/ios_cap_insets.json": <bytes>,
            ...
        }
    """
    width = source_image.width
    height = source_image.height

    # ── Shared assets (generated once, identical across scales) ──────

    preview_bytes: bytes | None = None
    nine_patch_bytes: bytes | None = None

    if outputs.get("previewPng", True):
        preview_img = render_nine_slice_preview(
            source_image,
            preview_options.get("targetWidth", width),
            preview_options.get("targetHeight", height),
            cap_insets,
        )
        buf = io.BytesIO()
        preview_img.save(buf, format="PNG")
        preview_bytes = buf.getvalue()

    if outputs.get("androidNinePatch", True):
        nine_patch_img = generate_nine_patch_image(
            source_image, cap_insets, content_insets,
        )
        buf = io.BytesIO()
        nine_patch_img.save(buf, format="PNG")
        nine_patch_bytes = buf.getvalue()

    # ── Per-scale artifacts ──────────────────────────────────────────

    file_map: Dict[str, bytes] = {}

    for scale in selected_scales:
        prefix = f"{scale}x"

        # Source PNG (same original for each scale folder)
        if outputs.get("sourcePng", True):
            file_map[f"{prefix}/source/bubble_original.png"] = original_bytes

        # Preview PNG
        if preview_bytes is not None:
            file_map[f"{prefix}/preview/bubble_preview.png"] = preview_bytes

        # Android .9.png
        if nine_patch_bytes is not None:
            file_map[f"{prefix}/android/bubble.9.png"] = nine_patch_bytes

        # Android JSON
        if outputs.get("androidJson", True):
            android_dict = build_android_json(
                image_id, width, height,
                scale, cap_insets, content_insets,
            )
            file_map[f"{prefix}/android/android_nine_patch.json"] = (
                json.dumps(android_dict, indent=2).encode("utf-8")
            )

        # iOS JSON
        if outputs.get("iosJson", True):
            ios_dict = build_ios_cap_insets_json(
                image_id, width, height,
                scale, cap_insets, content_insets,
            )
            file_map[f"{prefix}/ios/ios_cap_insets.json"] = (
                json.dumps(ios_dict, indent=2).encode("utf-8")
            )

        # README
        if outputs.get("readme", True):
            readme_text = build_readme(
                image_id, width, height,
                scale, cap_insets, content_insets,
            )
            file_map[f"{prefix}/README.md"] = readme_text.encode("utf-8")

    return file_map
