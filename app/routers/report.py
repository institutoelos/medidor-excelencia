"""Rota de geração do relatório (HTML + PDF via Playwright)."""
from __future__ import annotations

import asyncio
import os
import tempfile
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.content.items import (
    DEMO_CARGO,
    DEMO_TEMPO_CASA,
    ITENS_COLABORADOR,
    ITENS_SOCIO_DIVERGENTE,
    ITENS_SOCIO_ESPELHO,
    PILAR_LABEL,
    PILARES,
    RETENCAO_OPCOES,
    SUBPILAR_LABEL,
)
from app.models.db import Rodada, get_session
from app.services.engine import calcular_relatorio_completo

router = APIRouter()

_BASE = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(_BASE, "templates"))


@router.get("/relatorio/{rodada_id}", response_class=HTMLResponse)
def gerar_html(rodada_id: int, request: Request, db: Session = Depends(get_session)):
    try:
        dados = calcular_relatorio_completo(db, rodada_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    textos_colab = {i[0]: i[3] for i in ITENS_COLABORADOR}
    textos_socio = {i[0]: i[3] for i in (ITENS_SOCIO_ESPELHO + ITENS_SOCIO_DIVERGENTE)}
    return templates.TemplateResponse(
        "report/main.html",
        {
            "request": request,
            "d": dados,
            "PILARES": PILARES,
            "PILAR_LABEL": PILAR_LABEL,
            "SUBPILAR_LABEL": SUBPILAR_LABEL,
            "DEMO_CARGO": dict(DEMO_CARGO),
            "DEMO_TEMPO": dict(DEMO_TEMPO_CASA),
            "RETENCAO_OPCOES": dict(RETENCAO_OPCOES),
            "textos_colab": textos_colab,
            "textos_socio": textos_socio,
            "agora": datetime.now(),
        },
    )


@router.get("/relatorio/{rodada_id}/pdf")
async def gerar_pdf(rodada_id: int, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")

    # Gerar PDF via Playwright
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise HTTPException(status_code=500, detail="Playwright não instalado.")

    url = str(request.url_for("gerar_html", rodada_id=rodada_id))
    out_dir = os.path.join(_BASE, "..", "relatorios_gerados")
    os.makedirs(out_dir, exist_ok=True)
    nome_arquivo = f"relatorio_rodada_{rodada_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    out_path = os.path.abspath(os.path.join(out_dir, nome_arquivo))

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="load")
        # Esperar fontes Google carregarem
        try:
            await page.evaluate("document.fonts.ready")
        except Exception:
            pass
        await page.emulate_media(media="print")
        await page.pdf(
            path=out_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )
        await browser.close()

    return FileResponse(out_path, media_type="application/pdf", filename=nome_arquivo)
