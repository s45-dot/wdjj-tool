from pathlib import Path

# Base directory (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Upload directory
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

# Maximum upload size: 5 MB
MAX_UPLOAD_SIZE = 5 * 1024 * 1024

# Only PNG images allowed
ALLOWED_MIME = "image/png"
