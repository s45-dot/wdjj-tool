"""Download router for bubble stretch tool."""

import re
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import EXPORT_DIR

router = APIRouter()

# Validate file_id format: only alphanumeric, hyphens, and underscores
FILE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')


@router.get("/api/download/{file_id}")
async def download_export(file_id: str):
    """
    Download an exported ZIP file.

    Args:
        file_id: Unique identifier for the export file

    Returns:
        ZIP file download

    Raises:
        HTTPException: If file_id is invalid or file not found
    """
    # Validate file_id format
    if not FILE_ID_PATTERN.match(file_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid file_id format. Only alphanumeric characters, hyphens, and underscores are allowed."
        )

    # Construct expected ZIP path
    zip_path = EXPORT_DIR / "bubble_export.zip"

    # Check if file exists
    if not zip_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Export file not found"
        )

    # Return file for download
    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename="bubble_export.zip"
    )
