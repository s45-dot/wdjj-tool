#!/usr/bin/env python3
"""Bootstrap script for Bubble Stretch Tool.

Prints LAN address and QR-code info, then starts uvicorn on 0.0.0.0:8080.
"""

import sys
from pathlib import Path

# Ensure backend/ is on sys.path so ``import app.*`` works
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services import network_service, qrcode_service, token_service
from app.config import RUNTIME_DIR
from app.services.token_service import load_token, save_token

TOKEN_PATH = RUNTIME_DIR / "token.txt"


def print_banner():
    """Print LAN address and QR code URL to stdout."""
    info = network_service.get_lan_address()

    # Ensure a token exists
    if not TOKEN_PATH.exists():
        save_token(token_service.generate_token(), TOKEN_PATH)
    token = load_token(TOKEN_PATH)

    info["token"] = token
    print(f"\n🌐 Access URL: {info['url']}")
    print("📱 Scan QR code to open on mobile:")
    print(qrcode_service.generate_qrcode_data_url(info["url"]))
    print()


def main():
    print_banner()

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )


if __name__ == "__main__":
    main()
