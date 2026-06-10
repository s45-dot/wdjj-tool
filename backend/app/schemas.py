from pydantic import BaseModel


class HealthResponse(BaseModel):
    ok: bool
    version: str


class UploadResponse(BaseModel):
    imageId: str
    filename: str
    width: int
    height: int
    sizeBytes: int
    mimeType: str
    previewUrl: str
