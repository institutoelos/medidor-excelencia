"""Exportação CSV dos dados brutos de uma rodada (uso pós-fechamento).

Aplicamos anonimização defensiva no export:
- Recusa total se rodada tem menos de 5 respondentes (não dá agregado seguro).
- `lider_direto` (texto livre com nome de pessoa) é substituído por hash HMAC
  curto com salt por empresa — permite agrupar respostas por cohort de
  liderança sem revelar quem é o líder.
- Regra k≥5: pra cada linha, computamos o grupo (tempo_de_casa, tipo_de_cargo,
  area, lider_hash). Se esse grupo aparece em menos de 5 respondentes, mascaramos
  essas colunas como '[suprimido]'.
"""
from __future__ import annotations

import csv
import hmac
import hashlib
import io
import os
from collections import Counter
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.content.items import (
    ITENS_COLABORADOR,
    ITENS_SOCIO_DIVERGENTE,
    ITENS_SOCIO_ESPELHO,
)
from app.models.db import (
    Empresa,
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

_K_MIN = 5

# Secret pro hash de líder. Em produção vem de env; fallback derivado da senha.
_HASH_SECRET = os.environ.get("MEDIDOR_SESSION_SECRET") or os.environ.get("MEDIDOR_ADMIN_PASSWORD") or "medidor-v1"


def _hash_lider(empresa_id: int, lider: Optional[str]) -> str:
    """HMAC-SHA256(lider) com salt por empresa, truncado pra 8 chars. Permite
    agrupar respostas pelo mesmo líder sem revelar o nome."""
    if not lider or not lider.strip():
        return ""
    key = f"{_HASH_SECRET}::empresa_{empresa_id}".encode("utf-8")
    msg = lider.strip().lower().encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return f"lider_{digest[:8]}"


def _suprimir_se_k_baixo(linhas: list[dict], colunas_quasi: list[str]) -> list[dict]:
    """Aplica k≥5 nas colunas quasi-identifiers: linhas cujo grupo (combinação
    dos valores nessas colunas) tem menos de _K_MIN respondentes ficam com
    essas colunas mascaradas como '[suprimido]'.
    """
    chaves = [tuple(linha.get(c, "") for c in colunas_quasi) for linha in linhas]
    contagem = Counter(chaves)
    out = []
    for linha, chave in zip(linhas, chaves):
        nova = dict(linha)
        if contagem[chave] < _K_MIN:
            for c in colunas_quasi:
                nova[c] = "[suprimido]"
        out.append(nova)
    return out


def _csv_response(buf: io.StringIO, nome_arquivo: str) -> StreamingResponse:
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{nome_arquivo}"'},
    )


@router.get("/{rodada_id}/export/colab.csv")
def export_colab_csv(rodada_id: int, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")
    empresa: Empresa = rodada.empresa

    respondentes = (
        db.query(RespondenteColab)
        .filter(RespondenteColab.rodada_id == rodada_id, RespondenteColab.finalizado_em.isnot(None))
        .order_by(RespondenteColab.id)
        .all()
    )
    if len(respondentes) < _K_MIN:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Export bloqueado por anonimato: apenas {len(respondentes)} "
                f"respondentes finalizaram (mínimo {_K_MIN}). Aguarde mais respostas "
                "ou use o relatório PDF agregado, que já tem supressão automática."
            ),
        )

    quasi = ["tempo_de_casa", "tipo_de_cargo", "area", "lider_hash"]
    item_cols = [f"item_{i[0]}" for i in ITENS_COLABORADOR]

    linhas_brutas = []
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

        linha = {
            "respondente_id": r.id,
            "tempo_de_casa": r.tempo_de_casa or "",
            "tipo_de_cargo": r.tipo_de_cargo or "",
            "area": r.area or "",
            "lider_hash": _hash_lider(empresa.id, r.lider_direto),
            "ancora": ancora.valor if ancora else "",
            "nps": nps.valor_0_10 if nps else "",
            "retencao": ret.opcao_escolhida if ret else "",
            "retencao_outro": ret.texto_aberto if (ret and ret.texto_aberto) else "",
        }
        for i in ITENS_COLABORADOR:
            linha[f"item_{i[0]}"] = respostas.get(i[0], "")
        linhas_brutas.append(linha)

    linhas = _suprimir_se_k_baixo(linhas_brutas, quasi)

    buf = io.StringIO()
    cols = ["respondente_id"] + quasi + ["ancora", "nps", "retencao", "retencao_outro"] + item_cols
    writer = csv.writer(buf)
    writer.writerow(cols)
    for linha in linhas:
        writer.writerow([linha[c] for c in cols])

    return _csv_response(buf, f"rodada_{rodada_id}_colab.csv")


@router.get("/{rodada_id}/export/socio.csv")
def export_socio_csv(rodada_id: int, db: Session = Depends(get_session)):
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise HTTPException(status_code=404, detail="Rodada não encontrada.")

    respondentes = (
        db.query(RespondenteSocio)
        .filter(RespondenteSocio.rodada_id == rodada_id, RespondenteSocio.finalizado_em.isnot(None))
        .order_by(RespondenteSocio.id)
        .all()
    )
    # Sócios já tem N pequeno por design (1-2 normalmente); aqui mantemos o bloqueio
    # só se for 0 — o relatório agregado é onde fica a proteção.
    if not respondentes:
        raise HTTPException(
            status_code=404,
            detail="Nenhum sócio finalizou esta rodada ainda.",
        )

    buf = io.StringIO()
    writer = csv.writer(buf)
    todos = ITENS_SOCIO_ESPELHO + ITENS_SOCIO_DIVERGENTE
    cols = ["respondente_id", "ancora"] + [f"item_{i[0]}" for i in todos]
    writer.writerow(cols)

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

    return _csv_response(buf, f"rodada_{rodada_id}_socio.csv")
