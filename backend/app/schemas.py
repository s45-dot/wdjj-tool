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


class Insets(BaseModel):
    """Nine-patch insets for stretchable regions."""
    top: int
    right: int
    bottom: int
    left: int


class PreviewExportOptions(BaseModel):
    """Configuration for preview image export dimensions."""
    targetWidth: int
    targetHeight: int


class ExportOutputs(BaseModel):
    """Which output formats to generate during export."""
    androidNinePatch: bool = True
    iosJson: bool = True
    androidJson: bool = True
    previewPng: bool = True
    readme: bool = True
    sourcePng: bool = True


class ImageExportRequest(BaseModel):
    """Request body for exporting a nine-patch image."""
    imageId: str
    scale: int
    capInsets: Insets
    contentInsets: Insets
    preview: PreviewExportOptions
    outputs: ExportOutputs


class ExportResponse(BaseModel):
    """Response after successful export."""
    fileId: str
    filename: str
    downloadUrl: str


class ValidationMessage(BaseModel):
    """Validation error detail."""
    field: str
    message: str
    level: str
