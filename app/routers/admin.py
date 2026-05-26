"""Painel administrativo com autenticação, busca, parciais ao vivo, QR/link."""
from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.db import (
    Empresa,
    RespondenteColab,
    RespondenteSocio,
    Rodada,
    TIPOS_RODADA,
    get_session,
)
from app.services.auth import autenticar_admin
from app.services.engine import calcular_parciais_rodada
from app.services.qr import qr_svg

router = APIRouter(prefix="/admin", dependencies=[Depends(autenticar_admin)])

_BASE = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(_BASE, "templates"))


@router.get("")
@router.get("/")
def index(
    request: Request,
    q: str = Query("", description="Busca por nome de empresa"),
    db: Session = Depends(get_session),
):
    query = db.query(Empresa)
    if q.strip():
        like = f"%{q.strip()}%"
        query = query.filter(Empresa.nome.ilike(like))
    empresas = query.order_by(Empresa.data_entrada.desc()).all()

    parciais = {}  # rodada_id -> dict
    for e in empresas:
        for r in e.rodadas:
            parciais[r.id] = calcular_parciais_rodada(db, r.id)

    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "empresas": empresas,
            "parciais": parciais,
            "tipos_rodada": TIPOS_RODADA,
            "q": q,
        },
    )


@router.post("/empresas")
def criar_empresa(
    nome: str = Form(...),
    areas: str = Form(""),
    tamanho_time_esperado: str = Form(""),
    qtd_socios_esperados: str = Form("1"),
    db: Session = Depends(get_session),
):
    e = Empresa(
        nome=nome.strip(),
        lista_de_areas=areas.strip(),
        tamanho_time_esperado=int(tamanho_time_esperado) if tamanho_time_esperado.strip().isdigit() else None,
        qtd_socios_esperados=int(qtd_socios_esperados) if qtd_socios_esperados.strip().isdigit() else 1,
    )
    db.add(e)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/empresas/{empresa_id}/editar")
def editar_empresa(
    empresa_id: int,
    nome: str = Form(...),
    areas: str = Form(""),
    tamanho_time_esperado: str = Form(""),
    qtd_socios_esperados: str = Form("1"),
    db: Session = Depends(get_session),
):
    e = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if e is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    e.nome = nome.strip()
    e.lista_de_areas = areas.strip()
    e.tamanho_time_esperado = int(tamanho_time_esperado) if tamanho_time_esperado.strip().isdigit() else None
    e.qtd_socios_esperados = int(qtd_socios_esperados) if qtd_socios_esperados.strip().isdigit() else 1
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/empresas/{empresa_id}/rodadas")
def abrir_rodada(
    empresa_id: int,
    tipo: str = Form(...),
    db: Session = Depends(get_session),
):
    if tipo not in TIPOS_RODADA:
        raise HTTPException(status_code=400, detail="Tipo de rodada inválido.")
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    r = Rodada(empresa_id=empresa_id, tipo=tipo)
    db.add(r)
    db.commit()
    return RedirectResponse(url=f"/admin/rodadas/{r.id}", status_code=303)


@router.post("/rodadas/{rodada_id}/fechar")
def fechar(rodada_id: int, db: Session = Depends(get_session)):
    r = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if r is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    r.status = "fechada"
    r.data_fim = datetime.utcnow()
    db.commit()
    return RedirectResponse(url=f"/admin/rodadas/{rodada_id}", status_code=303)


@router.post("/rodadas/{rodada_id}/reabrir")
def reabrir(rodada_id: int, db: Session = Depends(get_session)):
    r = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if r is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    r.status = "aberta"
    r.data_fim = None
    db.commit()
    return RedirectResponse(url=f"/admin/rodadas/{rodada_id}", status_code=303)


@router.get("/rodadas/{rodada_id}")
def painel_rodada(rodada_id: int, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    parciais = calcular_parciais_rodada(db, rodada_id)
    base_url = str(request.base_url).rstrip("/")
    return templates.TemplateResponse(
        "admin/rodada.html",
        {
            "request": request,
            "rodada": rodada,
            "empresa": rodada.empresa,
            "parciais": parciais,
            "base_url": base_url,
            "link_colab": f"{base_url}/f/colab/{rodada.token_colab}",
            "link_socio": f"{base_url}/f/socio/{rodada.token_socio}",
        },
    )


@router.get("/qr")
def qr_link(url: str = Query(...), size: int = Query(220)):
    """QR code SVG para uma URL — usado nos cards de rodada."""
    svg = qr_svg(url, size_px=size)
    return Response(content=svg, media_type="image/svg+xml")


@router.get("/rodadas/{rodada_id}/parciais.json")
def parciais_json(rodada_id: int, db: Session = Depends(get_session)):
    """Endpoint JSON para polling de parciais (refresh ao vivo)."""
    p = calcular_parciais_rodada(db, rodada_id)
    return {
        "contagens": p.get("contagens", {}),
        "parciais": p.get("parciais"),
        "parciais_sao_relevantes": p.get("parciais_sao_relevantes", False),
    }
