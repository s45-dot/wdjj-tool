from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# ── Routers (API routes registered first, so they take priority) ─────

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(export.router)
app.include_router(download.router)
app.include_router(network.router)

# ── Token verification middleware ────────────────────────────────────


TOKEN_PATH = RUNTIME_DIR / "token.txt"

# Cache the token in memory; reload on each request for simplicity
# (file read is negligible at ~20 bytes per request)


def _load_stored_token() -> str | None:
    """Return the stored token, or None if the file doesn't exist."""
    try:
        return token_service.load_token(TOKEN_PATH).strip()
    except FileNotFoundError:
        return None


# Paths that never require a token
PUBLIC_PATH_PREFIXES = ("/api/health", "/api/network", "/uploads", "/")

# Protected API routes
PROTECTED_PATH_PREFIXES = ("/api/upload", "/api/export", "/api/download")


@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    """Verify X-Bubble-Token on protected API routes.

    Public paths (health, network, uploads, static) are always allowed.
    """
    # Always allow OPTIONS (CORS preflight) and unauthenticated paths
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path

    # Check if this is a protected route
    is_protected = any(path.startswith(p) for p in PROTECTED_PATH_PREFIXES)

    if is_protected:
        token = request.headers.get("X-Bubble-Token", "")
        stored = _load_stored_token()

        if not stored:
            return JSONResponse(
                status_code=500,
                content={"detail": "Server token not configured."},
            )

        if not token or token != stored:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing token."},
            )

    return await call_next(request)


# ── Static file serving (uploads) ────────────────────────────────────

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# ── Static frontend build (SPA fallback) ─────────────────────────────

FRONTEND_BUILD_DIR = Path(__file__).resolve().parent / "static" / "frontend_build"

if FRONTEND_BUILD_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_BUILD_DIR), html=True),
        name="frontend",
    )
else:
    print(
        f"⚠️  Frontend build not found at {FRONTEND_BUILD_DIR}.\n"
        f"   Run `scripts/build_frontend.sh` or use the Vite dev server.",
    )

# ── Startup hook: create token & print LAN info ──────────────────────


@app.on_event("startup")
async def startup():
    """Generate a token (if missing) and log LAN address."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    if not TOKEN_PATH.exists():
        token_service.save_token(
            token_service.generate_token(),
            TOKEN_PATH,
        )

    info = network_service.get_lan_address()
    print(f"🌐 Access URL: {info['url']}")
