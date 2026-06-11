"""Network endpoint – return LAN address and optional token."""

from fastapi import APIRouter

from app.services import network_service, token_service

router = APIRouter(prefix="/api/network", tags=["network"])


@router.get("")
async def get_network_info():
    """Return LAN address info.  If a token exists, embed it in the URL."""
    info = network_service.get_lan_address()

    # Append token to URL when available
    token = info.pop("token", None)
    url = info["url"]
    if token:
        url += f"?token={token}"
    info["url"] = url

    return info
