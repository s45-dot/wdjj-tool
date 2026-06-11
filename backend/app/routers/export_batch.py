"""Batch export router for Bubble Stretch Tool.

Processes multiple images with shared settings into a single ZIP archive.
"""

import uuid
from typing import Dict

from fastapi import APIRouter, HTTPException

from app.config import EXPORT_DIR, UPLOAD_DIR
from app.schemas import BatchExportRequest, ExportResponse
from app.services.image_loader import load_image_by_id
from app.services.multi_scale_export import export_multi_scale
from app.services.zip_exporter import create_multi_scale_export_zip

router = APIRouter()


@router.post("/api/export/batch", response_model=ExportResponse)
async def batch_export(request: BatchExportRequest):
    """
    Export multiple images as a single ZIP archive.

    For each image, generates multi-scale export artifacts using the
    provided insets and preview settings, then packages everything
    into one downloadable ZIP file.
    """
    if not request.images:
        raise HTTPException(status_code=400, detail="No images provided")

    if not request.selectedScales:
        raise HTTPException(status_code=400, detail="No scales selected")

    preview_options = {
        "targetWidth": request.preview.get("targetWidth", 240),
        "targetHeight": request.preview.get("targetHeight", 80),
    }

    outputs = {
        "androidNinePatch": True,
        "iosJson": True,
        "androidJson": True,
        "previewPng": True,
        "readme": True,
        "sourcePng": True,
    }

    all_files: Dict[str, bytes] = {}
    errors: list[Dict[str, str]] = []

    for item in request.images:
        image_id = item.imageId

        try:
            source_image, width, height = load_image_by_id(image_id)
        except FileNotFoundError:
            errors.append({"imageId": image_id, "error": "Image not found"})
            continue
        except ValueError as e:
            errors.append({"imageId": image_id, "error": str(e)})
            continue

        # Read original PNG bytes
        original_path = UPLOAD_DIR / f"{image_id}.png"
        original_bytes = original_path.read_bytes()

        try:
            file_map = export_multi_scale(
                image_id=image_id,
                source_image=source_image,
                original_bytes=original_bytes,
                cap_insets=dict(request.capInsets),
                content_insets=dict(request.contentInsets),
                selected_scales=list(request.selectedScales),
                preview_options=preview_options,
                outputs=outputs,
            )

            # Prefix each file with the image folder to avoid collisions
            for path, content in file_map.items():
                all_files[f"{image_id}/{path}"] = content

        except Exception as e:
            errors.append({"imageId": image_id, "error": str(e)})
            continue

    if not all_files:
        raise HTTPException(
            status_code=500,
            detail="All images failed processing. No files to export.",
        )

    # Create ZIP with batch prefix
    file_id = str(uuid.uuid4())
    create_multi_scale_export_zip(EXPORT_DIR, all_files)

    return ExportResponse(
        fileId=file_id,
        filename="batch_export.zip",
        downloadUrl=f"/api/download/{file_id}",
    )
