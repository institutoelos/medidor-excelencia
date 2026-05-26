"""QR code SVG simples — sem dependência externa.

Usa lib `qrcode` se disponível; senão, faz fallback para um SVG com placeholder.
Como `qrcode` é puro Python e já é dependência opcional comum, instalamos via pip.
"""
from __future__ import annotations

try:
    import qrcode
    import qrcode.image.svg
    _DISPONIVEL = True
except ImportError:
    _DISPONIVEL = False


def qr_svg(url: str, size_px: int = 220) -> str:
    """Gera SVG (string) de QR code para uma URL."""
    if not _DISPONIVEL:
        # Fallback: SVG com mensagem
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size_px}" height="{size_px}" viewBox="0 0 100 100">'
            f'<rect width="100" height="100" fill="#fff" stroke="#1a1a18" stroke-width="0.5"/>'
            f'<text x="50" y="50" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#1a1a18">'
            f'instale lib qrcode'
            f'</text></svg>'
        )
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(url, image_factory=factory, box_size=10, border=2)
    import io
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode("utf-8")
    # Ajusta atributos width/height para o tamanho desejado
    import re
    svg = re.sub(r'width="[^"]*"', f'width="{size_px}"', svg, count=1)
    svg = re.sub(r'height="[^"]*"', f'height="{size_px}"', svg, count=1)
    return svg
