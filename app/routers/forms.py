"""Rotas dos dois formulários (colaborador e sócio) com dedup por cookie."""
from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
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

# Em produção (HTTPS) marcamos o cookie como Secure. Liga via env var.
_COOKIE_SECURE = os.environ.get("MEDIDOR_COOKIE_SECURE", "").lower() in ("1", "true", "yes")


# ─── Agrupamento ───────────────────────────────────────────────────────

_SUBPILARES_ORDEM_COLAB = {
    PILAR_CULTURA: ["cultura_identidade", "cultura_tribo", "cultura_engajamento", "cultura_lideranca"],
    PILAR_EDUCACAO: ["educacao_estrutura", "educacao_qualidade"],
    PILAR_FEEDBACK: ["feedback_estrutura", "feedback_qualidade"],
}


def _itens_colab_agrupados():
    out = []
    for pilar in PILARES:
        secs = []
        for sub in _SUBPILARES_ORDEM_COLAB[pilar]:
            itens = [(i[0], i[3]) for i in ITENS_COLABORADOR if i[1] == pilar and i[2] == sub]
            secs.append((sub, SUBPILAR_LABEL[sub], itens))
        out.append((pilar, PILAR_LABEL[pilar], secs))
    return out


def _itens_socio_agrupados():
    out = []
    for pilar in PILARES:
        secs = []
        for sub in _SUBPILARES_ORDEM_COLAB[pilar]:
            itens = [(i[0], i[3]) for i in ITENS_SOCIO_ESPELHO if i[1] == pilar and i[2] == sub]
            if itens:
                secs.append((SUBPILAR_LABEL[sub] + " (observação do time)", itens))
        divs = [(i[0], i[3]) for i in ITENS_SOCIO_DIVERGENTE if i[1] == pilar]
        if divs:
            sub_div = "socio_consciencia_" + pilar
            secs.append((SUBPILAR_LABEL.get(sub_div, "Consciência sistêmica") + " (perguntas para o sócio)", divs))
        out.append((pilar, PILAR_LABEL[pilar], secs))
    return out


def _cookie_key(tipo: str, token: str) -> str:
    return f"med_{tipo}_{token}"


# ─── GET / POST colaborador ────────────────────────────────────────────

@router.get("/f/colab/{token}")
def render_form_colab(token: str, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.token_colab == token).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Link de formulário não encontrado.")
    if rodada.status == "fechada":
        return templates.TemplateResponse(
            "forms/fechada.html",
            {"request": request, "empresa": rodada.empresa, "rodada": rodada},
            status_code=410,
        )

    # Dedup: se já respondeu (cookie), mostra tela de "obrigado" no lugar do form
    cookie_val = request.cookies.get(_cookie_key("colab", token))
    if cookie_val:
        respondente = db.query(RespondenteColab).filter(RespondenteColab.sessao_token == cookie_val).first()
        if respondente and respondente.finalizado_em:
            return templates.TemplateResponse("forms/obrigado_colab.html", {
                "request": request,
                "empresa": rodada.empresa,
                "rodada": rodada,
                "finalizado_em": respondente.finalizado_em,
            })

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

    # Dedup pelo cookie: se já submeteu, redireciona pro form (vai mostrar "obrigado")
    cookie_val = request.cookies.get(_cookie_key("colab", token))
    if cookie_val:
        existente = db.query(RespondenteColab).filter(RespondenteColab.sessao_token == cookie_val).first()
        if existente and existente.finalizado_em:
            return RedirectResponse(url=f"/f/colab/{token}", status_code=303)

    form = await request.form()
    for num, *_ in ITENS_COLABORADOR:
        if not form.get(f"item_{num}"):
            raise HTTPException(status_code=400, detail=f"Item {num} obrigatório.")
    for campo in ("ancora", "nps", "retencao", "tempo_de_casa", "tipo_de_cargo", "area"):
        if not form.get(campo):
            raise HTTPException(status_code=400, detail=f"Campo {campo} obrigatório.")
    # Outro motivo obrigatório se marcou "outro"
    if form.get("retencao") == "outro" and not (form.get("retencao_outro") or "").strip():
        raise HTTPException(status_code=400, detail="Descreva o motivo se marcou 'Outro'.")

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
        texto_aberto=(form.get("retencao_outro") or "").strip() or None,
    ))
    db.commit()
    db.refresh(respondente)

    response = RedirectResponse(url=f"/f/colab/{token}", status_code=303)
    response.set_cookie(
        key=_cookie_key("colab", token),
        value=respondente.sessao_token,
        max_age=60 * 60 * 24 * 180,  # 180 dias
        httponly=True,
        samesite="lax",
        secure=_COOKIE_SECURE,
    )
    return response


# ─── GET / POST sócio ──────────────────────────────────────────────────

@router.get("/f/socio/{token}")
def render_form_socio(token: str, request: Request, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.token_socio == token).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Link de formulário não encontrado.")
    if rodada.status == "fechada":
        return templates.TemplateResponse(
            "forms/fechada.html",
            {"request": request, "empresa": rodada.empresa, "rodada": rodada},
            status_code=410,
        )

    cookie_val = request.cookies.get(_cookie_key("socio", token))
    if cookie_val:
        respondente = db.query(RespondenteSocio).filter(RespondenteSocio.sessao_token == cookie_val).first()
        if respondente and respondente.finalizado_em:
            return templates.TemplateResponse("forms/obrigado_socio.html", {
                "request": request,
                "empresa": rodada.empresa,
                "rodada": rodada,
                "finalizado_em": respondente.finalizado_em,
            })

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

    cookie_val = request.cookies.get(_cookie_key("socio", token))
    if cookie_val:
        existente = db.query(RespondenteSocio).filter(RespondenteSocio.sessao_token == cookie_val).first()
        if existente and existente.finalizado_em:
            return RedirectResponse(url=f"/f/socio/{token}", status_code=303)

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
    db.refresh(respondente)

    response = RedirectResponse(url=f"/f/socio/{token}", status_code=303)
    response.set_cookie(
        key=_cookie_key("socio", token),
        value=respondente.sessao_token,
        max_age=60 * 60 * 24 * 180,
        httponly=True,
        samesite="lax",
        secure=_COOKIE_SECURE,
    )
    return response


# Rota antiga (compat) — agora cada tipo tem sua própria tela
@router.get("/f/obrigado")
def obrigado_legacy(request: Request):
    return templates.TemplateResponse("forms/obrigado.html", {"request": request})
