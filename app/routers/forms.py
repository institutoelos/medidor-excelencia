"""Rotas dos dois formulários (colaborador e sócio)."""
from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.content.items import (
    ANCORA_COLABORADOR,
    ANCORA_SOCIO,
    DEMO_CARGO,
    DEMO_TEMPO_CASA,
    ITENS_COLABORADOR,
    ITENS_SOCIO_DIVERGENTE,
    ITENS_SOCIO_ESPELHO,
    LIKERT_OPCOES,
    NPS_PERGUNTA,
    PILAR_CULTURA,
    PILAR_EDUCACAO,
    PILAR_FEEDBACK,
    PILAR_LABEL,
    PILARES,
    RETENCAO_OPCOES,
    RETENCAO_PERGUNTA,
    SUBPILAR_LABEL,
)
from app.models.db import (
    RespondenteColab,
    RespondenteSocio,
    Resposta,
    RespostaAncora,
    RespostaNPS,
    RespostaRetencao,
    Rodada,
    get_session,
)

router = APIRouter()

_BASE = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(_BASE, "templates"))


# ─── Agrupamento para template ─────────────────────────────────────────

_SUBPILARES_ORDEM_COLAB = {
    PILAR_CULTURA: ["cultura_identidade", "cultura_tribo", "cultura_engajamento", "cultura_lideranca"],
    PILAR_EDUCACAO: ["educacao_estrutura", "educacao_qualidade"],
    PILAR_FEEDBACK: ["feedback_estrutura", "feedback_qualidade"],
}


def _itens_colab_agrupados():
    """[(pilar_cod, pilar_label, [(sub_cod, sub_label, [(num, texto)])])]"""
    out = []
    for pilar in PILARES:
        secs = []
        for sub in _SUBPILARES_ORDEM_COLAB[pilar]:
            itens = [(i[0], i[3]) for i in ITENS_COLABORADOR if i[1] == pilar and i[2] == sub]
            secs.append((sub, SUBPILAR_LABEL[sub], itens))
        out.append((pilar, PILAR_LABEL[pilar], secs))
    return out


def _itens_socio_agrupados():
    """Mostra primeiro os 41 espelho por pilar, depois os 17 divergentes por pilar."""
    out = []
    for pilar in PILARES:
        secs = []
        # Espelho do pilar — agrupados por subpilar (mesmos do colab)
        for sub in _SUBPILARES_ORDEM_COLAB[pilar]:
            itens = [(i[0], i[3]) for i in ITENS_SOCIO_ESPELHO if i[1] == pilar and i[2] == sub]
            if itens:
                secs.append((SUBPILAR_LABEL[sub] + " (observação do time)", itens))
        # Divergentes do pilar
        divs = [(i[0], i[3]) for i in ITENS_SOCIO_DIVERGENTE if i[1] == pilar]
        if divs:
            sub_div = "socio_consciencia_" + pilar
            secs.append((SUBPILAR_LABEL.get(sub_div, "Consciência sistêmica") + " (perguntas para o sócio)", divs))
        out.append((pilar, PILAR_LABEL[pilar], secs))
    return out


# ─── GET formulário colaborador ───────────────────────────────────────

@router.get("/f/colab/{token}")
def render_form_colab(token: str, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.token_colab == token).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Link de formulário não encontrado.")
    if rodada.status == "fechada":
        return templates.TemplateResponse("forms/fechada.html", {"request": request, "empresa": rodada.empresa, "rodada": rodada}, status_code=410)
    return templates.TemplateResponse(
        "forms/colab.html",
        {
            "request": request,
            "token": token,
            "empresa": rodada.empresa,
            "itens_agrupados": _itens_colab_agrupados(),
            "likert": LIKERT_OPCOES,
            "ancora_texto": ANCORA_COLABORADOR,
            "nps_pergunta": NPS_PERGUNTA,
            "retencao_pergunta": RETENCAO_PERGUNTA,
            "retencao_opcoes": RETENCAO_OPCOES,
            "demo_tempo": DEMO_TEMPO_CASA,
            "demo_cargo": DEMO_CARGO,
        },
    )


@router.post("/f/colab/{token}/enviar")
async def submit_form_colab(token: str, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.token_colab == token).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    if rodada.status == "fechada":
        raise HTTPException(status_code=410, detail="A coleta desta rodada já foi encerrada.")
    form = await request.form()

    # Validação: 58 itens + âncora + nps + retenção + 3 demográficos
    for num, *_ in ITENS_COLABORADOR:
        if not form.get(f"item_{num}"):
            raise HTTPException(status_code=400, detail=f"Item {num} obrigatório.")
    for campo in ("ancora", "nps", "retencao", "tempo_de_casa", "tipo_de_cargo", "area"):
        if not form.get(campo):
            raise HTTPException(status_code=400, detail=f"Campo {campo} obrigatório.")

    respondente = RespondenteColab(
        rodada_id=rodada.id,
        tempo_de_casa=form.get("tempo_de_casa"),
        tipo_de_cargo=form.get("tipo_de_cargo"),
        area=form.get("area"),
        finalizado_em=datetime.utcnow(),
    )
    db.add(respondente)
    db.flush()

    for num, *_ in ITENS_COLABORADOR:
        valor = int(form.get(f"item_{num}"))
        if valor < 1 or valor > 5:
            raise HTTPException(status_code=400, detail=f"Valor inválido no item {num}.")
        db.add(Resposta(
            respondente_id=respondente.id,
            tipo_respondente="colab",
            item_numero=num,
            valor_likert=valor,
        ))
    db.add(RespostaAncora(
        respondente_id=respondente.id,
        tipo_respondente="colab",
        valor=int(form.get("ancora")),
    ))
    db.add(RespostaNPS(
        respondente_id=respondente.id,
        valor_0_10=int(form.get("nps")),
    ))
    db.add(RespostaRetencao(
        respondente_id=respondente.id,
        opcao_escolhida=form.get("retencao"),
        texto_aberto=form.get("retencao_outro") or None,
    ))
    db.commit()
    return RedirectResponse(url="/f/obrigado", status_code=303)


# ─── GET formulário sócio ─────────────────────────────────────────────

@router.get("/f/socio/{token}")
def render_form_socio(token: str, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.token_socio == token).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Link de formulário não encontrado.")
    if rodada.status == "fechada":
        return templates.TemplateResponse("forms/fechada.html", {"request": request, "empresa": rodada.empresa, "rodada": rodada}, status_code=410)
    return templates.TemplateResponse(
        "forms/socio.html",
        {
            "request": request,
            "token": token,
            "empresa": rodada.empresa,
            "agrupado": _itens_socio_agrupados(),
            "likert": LIKERT_OPCOES,
            "ancora_texto": ANCORA_SOCIO,
        },
    )


@router.post("/f/socio/{token}/enviar")
async def submit_form_socio(token: str, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.token_socio == token).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    if rodada.status == "fechada":
        raise HTTPException(status_code=410, detail="A coleta desta rodada já foi encerrada.")
    form = await request.form()

    todos = ITENS_SOCIO_ESPELHO + ITENS_SOCIO_DIVERGENTE
    for i in todos:
        num = i[0]
        if not form.get(f"item_{num}"):
            raise HTTPException(status_code=400, detail=f"Item {num} obrigatório.")
    if not form.get("ancora"):
        raise HTTPException(status_code=400, detail="Âncora obrigatória.")

    respondente = RespondenteSocio(rodada_id=rodada.id, finalizado_em=datetime.utcnow())
    db.add(respondente)
    db.flush()

    for i in todos:
        num = i[0]
        valor = int(form.get(f"item_{num}"))
        if valor < 1 or valor > 5:
            raise HTTPException(status_code=400, detail=f"Valor inválido no item {num}.")
        db.add(Resposta(
            respondente_id=respondente.id,
            tipo_respondente="socio",
            item_numero=num,
            valor_likert=valor,
        ))
    db.add(RespostaAncora(
        respondente_id=respondente.id,
        tipo_respondente="socio",
        valor=int(form.get("ancora")),
    ))
    db.commit()
    return RedirectResponse(url="/f/obrigado", status_code=303)


@router.get("/f/obrigado")
def obrigado(request: Request):
    return templates.TemplateResponse("forms/obrigado.html", {"request": request})
