"""Exportação CSV dos dados brutos de uma rodada (uso pós-fechamento)."""
from __future__ import annotations

import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.content.items import (
    ITENS_COLABORADOR,
    ITENS_SOCIO_DIVERGENTE,
    ITENS_SOCIO_ESPELHO,
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
from app.services.auth import autenticar_admin

router = APIRouter(prefix="/admin/rodadas", dependencies=[Depends(autenticar_admin)])


@router.get("/{rodada_id}/export/colab.csv")
def export_colab_csv(rodada_id: int, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")

    buf = io.StringIO()
    writer = csv.writer(buf)
    cols = ["respondente_id", "tempo_de_casa", "tipo_de_cargo", "area", "ancora", "nps", "retencao", "retencao_outro"]
    cols += [f"item_{i[0]}" for i in ITENS_COLABORADOR]
    writer.writerow(cols)

    respondentes = (
        db.query(RespondenteColab)
        .filter(RespondenteColab.rodada_id == rodada_id, RespondenteColab.finalizado_em.isnot(None))
        .order_by(RespondenteColab.id)
        .all()
    )
    for r in respondentes:
        respostas = {
            row.item_numero: row.valor_likert
            for row in db.query(Resposta).filter(
                Resposta.respondente_id == r.id, Resposta.tipo_respondente == "colab"
            ).all()
        }
        ancora = db.query(RespostaAncora).filter(
            RespostaAncora.respondente_id == r.id, RespostaAncora.tipo_respondente == "colab"
        ).first()
        nps = db.query(RespostaNPS).filter(RespostaNPS.respondente_id == r.id).first()
        ret = db.query(RespostaRetencao).filter(RespostaRetencao.respondente_id == r.id).first()
        linha = [
            r.id, r.tempo_de_casa, r.tipo_de_cargo, r.area,
            ancora.valor if ancora else "",
            nps.valor_0_10 if nps else "",
            ret.opcao_escolhida if ret else "",
            ret.texto_aberto if (ret and ret.texto_aberto) else "",
        ]
        linha += [respostas.get(i[0], "") for i in ITENS_COLABORADOR]
        writer.writerow(linha)

    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="rodada_{rodada_id}_colab.csv"'},
    )


@router.get("/{rodada_id}/export/socio.csv")
def export_socio_csv(rodada_id: int, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")

    buf = io.StringIO()
    writer = csv.writer(buf)
    todos = ITENS_SOCIO_ESPELHO + ITENS_SOCIO_DIVERGENTE
    cols = ["respondente_id", "ancora"] + [f"item_{i[0]}" for i in todos]
    writer.writerow(cols)

    respondentes = (
        db.query(RespondenteSocio)
        .filter(RespondenteSocio.rodada_id == rodada_id, RespondenteSocio.finalizado_em.isnot(None))
        .order_by(RespondenteSocio.id)
        .all()
    )
    for r in respondentes:
        respostas = {
            row.item_numero: row.valor_likert
            for row in db.query(Resposta).filter(
                Resposta.respondente_id == r.id, Resposta.tipo_respondente == "socio"
            ).all()
        }
        ancora = db.query(RespostaAncora).filter(
            RespostaAncora.respondente_id == r.id, RespostaAncora.tipo_respondente == "socio"
        ).first()
        linha = [r.id, ancora.valor if ancora else ""]
        linha += [respostas.get(i[0], "") for i in todos]
        writer.writerow(linha)

    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="rodada_{rodada_id}_socio.csv"'},
    )
