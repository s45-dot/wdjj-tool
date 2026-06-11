"""Network utilities for LAN discovery and token management."""

import socket


def get_lan_address() -> dict:
    """Return LAN IP, port, and full URL for local network access.

    Tries to find a non-loopback IPv4 address using socket.gethostbyname(),
    then falls back to 127.0.0.1 if no LAN interface is available.
    """
    port = 8080

    # Attempt to resolve hostname to an IP
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except OSError:
        ip = "127.0.0.1"

    # Reject loopback; fall back to localhost
    if ip.startswith("127."):
        ip = "127.0.0.1"

    return {
        "host": ip,
        "port": port,
        "url": f"http://{ip}:{port}",
    }
