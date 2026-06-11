#!/usr/bin/env python3
"""Start the Bubble Stretch Tool backend server."""

import argparse
import sys
import webbrowser
from pathlib import Path


def get_lan_ip():
    """Get the LAN IP address."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def check_port(port=8080):
    """Check if port is available."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.bind(("0.0.0.0", port))
        sock.close()
        return True
    except OSError:
        sock.close()
        return False


def main():
    parser = argparse.ArgumentParser(description="Start Bubble Stretch Tool backend")
    parser.add_argument("--no-browser", action="store_true", help="Skip opening browser")
    args = parser.parse_args()

    port = 8080

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

    if not check_port(port):
        print(f"Port {port} is in use. Please stop the existing service or use a different port.")
        sys.exit(1)

    local_url = "http://127.0.0.1:8080"
    print(f"Starting server on {local_url}")

    lan_ip = get_lan_ip()
    lan_url = f"http://{lan_ip}:{port}"
    print(f"🌐 Mobile access: {lan_url}")

    if not args.no_browser:
        webbrowser.open(local_url)

    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()