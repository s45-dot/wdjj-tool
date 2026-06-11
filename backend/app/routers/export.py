"""Export router for bubble stretch tool."""

import io
import json
import uuid

from fastapi import APIRouter, HTTPException

from app.config import EXPORT_DIR, UPLOAD_DIR
from app.schemas import ExportResponse, ImageExportRequest
from app.services.android_export import build_android_json
from app.services.image_loader import load_image_by_id
from app.services.ios_export import build_ios_cap_insets_json
from app.services.multi_scale_export import export_multi_scale
from app.services.nine_patch import generate_nine_patch_image
from app.services.preview_renderer import render_nine_slice_preview
from app.services.readme_export import build_readme
from app.services.zip_exporter import (
    create_export_zip,
    create_multi_scale_export_zip,
)

router = APIRouter()


@router.post("/api/export", response_model=ExportResponse)
async def export_image(request: ImageExportRequest):
    """
    Export image assets as a ZIP file.

    Supports two modes:
    - Single-scale (legacy): uses request.scale for a single export.
    - Multi-scale: uses request.selectedScales to generate per-scale artifacts.
    """
    # ── Determine whether to run multi-scale ─────────────────────────
    selected_scales = request.selectedScales

    if selected_scales and len(selected_scales) > 1:
        return await _multi_scale_export(request, selected_scales)

    # ── Single-scale (original path) ─────────────────────────────────
    scale = selected_scales[0] if selected_scales else request.scale
    try:
        source_image, width, height = load_image_by_id(request.imageId)
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail=f"Image not found: {request.imageId}",
        )

    try:
        original_path = UPLOAD_DIR / f"{request.imageId}.png"
        original_bytes = original_path.read_bytes()

        cap_insets = {
            "top": request.capInsets.top,
            "right": request.capInsets.right,
            "bottom": request.capInsets.bottom,
            "left": request.capInsets.left,
        }
        content_insets = {
            "top": request.contentInsets.top,
            "right": request.contentInsets.right,
            "bottom": request.contentInsets.bottom,
            "left": request.contentInsets.left,
        }

        # 4. Render preview PNG
        preview_img = render_nine_slice_preview(
            source_image,
            request.preview.targetWidth,
            request.preview.targetHeight,
            cap_insets,
        )
        preview_buf = io.BytesIO()
        preview_img.save(preview_buf, format="PNG")
        preview_bytes = preview_buf.getvalue()

        # 5. Generate .9.png
        nine_patch_img = generate_nine_patch_image(
            source_image, cap_insets, content_insets,
        )
        nine_patch_buf = io.BytesIO()
        nine_patch_img.save(nine_patch_buf, format="PNG")
        nine_patch_bytes = nine_patch_buf.getvalue()

        # 6. Build iOS JSON
        ios_dict = build_ios_cap_insets_json(
            request.imageId, width, height,
            scale, cap_insets, content_insets,
        )
        ios_json_bytes = json.dumps(ios_dict, indent=2).encode("utf-8")

        # 7. Build Android JSON
        android_dict = build_android_json(
            request.imageId, width, height,
            scale, cap_insets, content_insets,
        )
        android_json_bytes = json.dumps(android_dict, indent=2).encode("utf-8")

        # 8. Build README
        readme_text = build_readme(
            request.imageId, width, height,
            scale, cap_insets, content_insets,
        )
        readme_bytes = readme_text.encode("utf-8")

        # 9. Create ZIP with all 6 files
        file_id = str(uuid.uuid4())
        create_export_zip(EXPORT_DIR, {
            "source/bubble_original.png": original_bytes,
            "preview/bubble_preview.png": preview_bytes,
            "android/bubble.9.png": nine_patch_bytes,
            "android/android_nine_patch.json": android_json_bytes,
            "ios/ios_cap_insets.json": ios_json_bytes,
            "README.md": readme_bytes,
        })

        return ExportResponse(
            fileId=file_id,
            filename="bubble_export.zip",
            downloadUrl=f"/api/download/{file_id}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}",
        )


async def _multi_scale_export(
    request: ImageExportRequest,
    selected_scales: list[int],
) -> ExportResponse:
    """Handle multi-scale export by delegating to multi_scale_export service."""
    try:
        source_image, width, height = load_image_by_id(request.imageId)
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail=f"Image not found: {request.imageId}",
        )

    try:
        original_path = UPLOAD_DIR / f"{request.imageId}.png"
        original_bytes = original_path.read_bytes()

        cap_insets = {
            "top": request.capInsets.top,
            "right": request.capInsets.right,
            "bottom": request.capInsets.bottom,
            "left": request.capInsets.left,
        }
        content_insets = {
            "top": request.contentInsets.top,
            "right": request.contentInsets.right,
            "bottom": request.contentInsets.bottom,
            "left": request.contentInsets.left,
        }

        outputs = {
            "androidNinePatch": request.outputs.androidNinePatch,
            "iosJson": request.outputs.iosJson,
            "androidJson": request.outputs.androidJson,
            "previewPng": request.outputs.previewPng,
            "readme": request.outputs.readme,
            "sourcePng": request.outputs.sourcePng,
        }

        file_map = export_multi_scale(
            image_id=request.imageId,
            source_image=source_image,
            original_bytes=original_bytes,
            cap_insets=cap_insets,
            content_insets=content_insets,
            selected_scales=selected_scales,
            preview_options={
                "targetWidth": request.preview.targetWidth,
                "targetHeight": request.preview.targetHeight,
            },
            outputs=outputs,
        )

        file_id = str(uuid.uuid4())
        create_multi_scale_export_zip(EXPORT_DIR, file_map)

        return ExportResponse(
            fileId=file_id,
            filename="bubble_multi_export.zip",
            downloadUrl=f"/api/download/{file_id}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}",
        )
