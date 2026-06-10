import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

from app.config import ALLOWED_MIME, MAX_UPLOAD_SIZE, UPLOAD_DIR
from app.schemas import UploadResponse
from app.services.image_loader import load_and_validate

router = APIRouter()


@router.post("/api/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    # ── MIME type check ──────────────────────────────────────────────
    if file.content_type != ALLOWED_MIME:
        raise HTTPException(
            status_code=400,
            detail=f"Only PNG images are allowed. Got: {file.content_type}",
        )

    # ── Read content ─────────────────────────────────────────────────
    content = await file.read()

    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_UPLOAD_SIZE // (1024 * 1024)} MB.",
        )

    # ── Save to disk ─────────────────────────────────────────────────
    file_id = str(uuid.uuid4())
    ext = Path(file.filename or "image.png").suffix or ".png"
    dest_filename = f"{file_id}{ext}"
    dest_path = UPLOAD_DIR / dest_filename

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    dest_path.write_bytes(content)

    # ── Validate image with Pillow ───────────────────────────────────
    try:
        info = load_and_validate(dest_path)
    except ValueError as exc:
        # Remove the saved file since it's invalid
        dest_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return UploadResponse(
        imageId=file_id,
        filename=file.filename or dest_filename,
        width=info["width"],
        height=info["height"],
        sizeBytes=len(content),
        mimeType="image/png",
        previewUrl=f"/uploads/{dest_filename}",
    )
