"""QR-code generation utilities (no temp files, inline data URLs)."""

import base64
import io

from qrcode import make as qrcode_make


def generate_qrcode_data_url(url: str) -> str:
    """Generate a base64 data URL for a QR code containing *url*.

    Returns ``"data:image/png;base64,..."`` ready to embed in HTML.
    """
    qr = qrcode_make(url)

    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    b64 = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"
