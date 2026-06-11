from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import UPLOAD_DIR, RUNTIME_DIR
from app.routers import health, upload, export, download, network
from app.services import network_service, token_service

app = FastAPI(title="Bubble Stretch Tool API", version="0.1.0")

# CORS – allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(export.router)
app.include_router(download.router)
app.include_router(network.router)

# Serve uploaded files statically
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# ── Startup hook: create token & print LAN info ──────────────────────


@app.on_event("startup")
async def startup():
    """Generate a token (if missing) and log LAN address."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    if not (RUNTIME_DIR / "token.txt").exists():
        token_service.save_token(
            token_service.generate_token(),
            RUNTIME_DIR / "token.txt",
        )

    info = network_service.get_lan_address()
    print(f"🌐 Access URL: {info['url']}")
