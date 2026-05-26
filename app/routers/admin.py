"""Painel administrativo."""
from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.db import (
    Empresa,
    RespondenteColab,
    RespondenteSocio,
    Rodada,
    TIPOS_RODADA,
    get_session,
)

router = APIRouter(prefix="/admin")

_BASE = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(_BASE, "templates"))


@router.get("")
@router.get("/")
def index(request: Request, db: Session = Depends(get_session)):
    empresas = db.query(Empresa).order_by(Empresa.data_entrada.desc()).all()
    contagens = {}
    for e in empresas:
        for r in e.rodadas:
            n_colab = db.query(RespondenteColab).filter(
                RespondenteColab.rodada_id == r.id,
                RespondenteColab.finalizado_em.isnot(None),
            ).count()
            n_socio = db.query(RespondenteSocio).filter(
                RespondenteSocio.rodada_id == r.id,
                RespondenteSocio.finalizado_em.isnot(None),
            ).count()
            contagens[r.id] = type("C", (), {"colaboradores": n_colab, "socios": n_socio})
    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
            "empresas": empresas,
            "contagens": contagens,
            "tipos_rodada": TIPOS_RODADA,
        },
    )


@router.post("/empresas")
def criar_empresa(
    nome: str = Form(...),
    areas: str = Form(""),
    db: Session = Depends(get_session),
):
    e = Empresa(nome=nome.strip(), lista_de_areas=areas.strip())
    db.add(e)
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
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/rodadas/{rodada_id}/fechar")
def fechar(rodada_id: int, db: Session = Depends(get_session)):
    r = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if r is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    r.status = "fechada"
    r.data_fim = datetime.utcnow()
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/rodadas/{rodada_id}/reabrir")
def reabrir(rodada_id: int, db: Session = Depends(get_session)):
    r = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if r is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    r.status = "aberta"
    r.data_fim = None
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)
