"""Engine de cálculo do Medidor de Excelência ELOS — Pilar Pessoas.

Implementa todas as métricas da seção 11 da especificação:
- Top 2 Box por item
- Média ponderada por item
- Nota por pilar
- Medidor de Excelência (índice geral 0–100)
- eNPS (% Promotores − % Detratores)
- Gap por item espelho
- Índice de Consciência Sistêmica
- Cortes demográficos com regra de 5+ respondentes

PRINCÍPIOS NÃO NEGOCIÁVEIS (§17):
1. eNPS é calculado pela fórmula correta. NUNCA média aritmética.
2. Cortes < 5 respondentes não reportam.
3. Especificidade em prosa (n de total).
4. Gate visual NÃO altera o número do Medidor.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.content.items import (
    ITENS_COLABORADOR,
    ITENS_SOCIO_DIVERGENTE,
    ITENS_SOCIO_ESPELHO,
    PILAR_CULTURA,
    PILAR_EDUCACAO,
    PILAR_FEEDBACK,
    PILAR_LABEL,
    PILARES,
    faixa_do_medidor,
)
from app.models.db import (
    RespondenteColab,
    RespondenteSocio,
    Resposta,
    RespostaAncora,
    RespostaNPS,
    RespostaRetencao,
    Rodada,
)

MINIMO_PARA_REPORTAR_CORTE = 5  # §17.2


def comparar_com_anterior(db: Session, rodada_id: int) -> Optional[dict]:
    """Compara a rodada atual com a anterior da mesma empresa (se houver).

    Retorna None se for a primeira rodada. Itens com regressão > 10 são
    sinalizados (§15.2).
    """
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        return None
    anterior = (
        db.query(Rodada)
        .filter(Rodada.empresa_id == rodada.empresa_id, Rodada.id != rodada_id, Rodada.id < rodada_id)
        .order_by(Rodada.id.desc())
        .first()
    )
    if anterior is None:
        return None

    # Métricas atuais e anteriores
    def _calc(rid):
        respostas = _respostas_likert_por_item(db, rid, "colab")
        pilares = calcular_pilares_colab(respostas)
        notas = {p: pilares[p]["nota_pilar"] for p in PILARES}
        medidor = calcular_medidor(notas)
        # NPS
        ids = [r.id for r in db.query(RespondenteColab).filter(RespondenteColab.rodada_id == rid).all()]
        nps_vals = [r[0] for r in db.query(RespostaNPS.valor_0_10).filter(RespostaNPS.respondente_id.in_(ids)).all()] if ids else []
        enps = calcular_enps(nps_vals)["enps"]
        return {"medidor": medidor, "pilares": notas, "enps": enps, "pilares_por_item": {p: pilares[p]["top2_por_item"] for p in PILARES}}

    atual = _calc(rodada_id)
    prev = _calc(anterior.id)

    def _diff(a, b):
        if a is None or b is None:
            return None
        return round(a - b, 1)

    diffs = {
        "medidor": _diff(atual["medidor"], prev["medidor"]),
        "pilares": {p: _diff(atual["pilares"][p], prev["pilares"][p]) for p in PILARES},
        "enps": _diff(atual["enps"], prev["enps"]),
    }

    # Regressões por item > 10 p.p.
    regressoes = []
    for p in PILARES:
        for num, t2_atual in atual["pilares_por_item"][p].items():
            t2_prev = prev["pilares_por_item"][p].get(num)
            if t2_atual is None or t2_prev is None:
                continue
            d = t2_atual - t2_prev
            if d <= -10:
                regressoes.append({"num": num, "pilar": p, "atual": t2_atual, "anterior": t2_prev, "delta": round(d, 1)})
    regressoes.sort(key=lambda r: r["delta"])

    return {
        "rodada_anterior": {"id": anterior.id, "tipo": anterior.tipo, "data": anterior.data_inicio},
        "rodada_atual": {"id": rodada_id, "tipo": rodada.tipo, "data": rodada.data_inicio},
        "atual": atual,
        "anterior": prev,
        "diffs": diffs,
        "regressoes_acima_10": regressoes,
    }


def calcular_parciais_rodada(db: Session, rodada_id: int) -> dict:
    """Painel parcial enquanto a rodada está aberta: contagem, ritmo, médias por pilar.

    Não substitui o relatório fechado — serve só pro mentor acompanhar a coleta.
    """
    from datetime import datetime, timedelta
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        return {}

    respondentes_colab = (
        db.query(RespondenteColab)
        .filter(RespondenteColab.rodada_id == rodada_id)
        .all()
    )
    respondentes_socio = (
        db.query(RespondenteSocio)
        .filter(RespondenteSocio.rodada_id == rodada_id)
        .all()
    )
    n_colab = len(respondentes_colab)
    n_socio = len(respondentes_socio)

    esperado_colab = rodada.empresa.tamanho_time_esperado
    esperado_socio = rodada.empresa.qtd_socios_esperados or 1
    pct_colab = (round(n_colab / esperado_colab * 100, 1) if esperado_colab else None)
    pct_socio = round(n_socio / esperado_socio * 100, 1) if esperado_socio else None

    # Ritmo nas últimas 24h
    agora = datetime.utcnow()
    ult_24h = agora - timedelta(hours=24)
    ult_24h_colab = sum(1 for r in respondentes_colab if r.criado_em and r.criado_em >= ult_24h)
    ult_24h_socio = sum(1 for r in respondentes_socio if r.criado_em and r.criado_em >= ult_24h)

    # Médias parciais (Top 2 Box por pilar, colab apenas)
    respostas_colab_map = _respostas_likert_por_item(db, rodada_id, "colab")
    pilares_colab_parcial = calcular_pilares_colab(respostas_colab_map)
    notas_parciais = {p: pilares_colab_parcial[p]["nota_pilar"] for p in PILARES}
    medidor_parcial = calcular_medidor(notas_parciais)

    return {
        "rodada_id": rodada_id,
        "rodada_tipo": rodada.tipo,
        "rodada_status": rodada.status,
        "rodada_inicio": rodada.data_inicio,
        "empresa_nome": rodada.empresa.nome,
        "contagens": {
            "colab": n_colab,
            "colab_esperado": esperado_colab,
            "colab_pct": pct_colab,
            "socio": n_socio,
            "socio_esperado": esperado_socio,
            "socio_pct": pct_socio,
            "ult_24h_colab": ult_24h_colab,
            "ult_24h_socio": ult_24h_socio,
        },
        "parciais": {
            "medidor": medidor_parcial,
            "pilares": notas_parciais,
            "faixa": faixa_do_medidor(medidor_parcial) if medidor_parcial is not None else None,
        } if n_colab > 0 else None,
        "minimo_para_parciais_relevantes": 5,
        "parciais_sao_relevantes": n_colab >= 5,
    }


# ─── Funções puras (cálculo) ────────────────────────────────────────────────

def calcular_top2box(valores: Iterable[int]) -> Optional[float]:
    valores = list(valores)
    if not valores:
        return None
    top2 = sum(1 for v in valores if v in (4, 5))
    return round(top2 / len(valores) * 100, 1)


def calcular_media_ponderada(valores: Iterable[int]) -> Optional[float]:
    valores = list(valores)
    if not valores:
        return None
    return round(sum(valores) / len(valores), 2)


def calcular_distribuicao(valores: Iterable[int]) -> dict[int, int]:
    """Contagem absoluta de cada nota 1..5. Itens sem resposta = todos zero."""
    contagem = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for v in valores:
        if v in contagem:
            contagem[v] += 1
    return contagem


def calcular_enps(notas_0_10: Iterable[int]) -> dict:
    """Fórmula correta NPS: % Promotores (9–10) − % Detratores (0–6).

    Retorna dict com promotores/neutros/detratores e enps (-100..100).
    Se vazio, retorna estrutura com enps=None e todos zerados.
    """
    notas = list(notas_0_10)
    total = len(notas)
    if total == 0:
        return {
            "total": 0,
            "promotores": 0, "neutros": 0, "detratores": 0,
            "pct_promotores": None, "pct_neutros": None, "pct_detratores": None,
            "enps": None,
        }
    promotores = sum(1 for n in notas if n >= 9)
    detratores = sum(1 for n in notas if n <= 6)
    neutros = total - promotores - detratores
    pct_p = promotores / total * 100
    pct_d = detratores / total * 100
    pct_n = neutros / total * 100
    enps = round(pct_p - pct_d, 1)
    return {
        "total": total,
        "promotores": promotores, "neutros": neutros, "detratores": detratores,
        "pct_promotores": round(pct_p, 1),
        "pct_neutros": round(pct_n, 1),
        "pct_detratores": round(pct_d, 1),
        "enps": enps,
    }


def calcular_nota_pilar(top2box_por_item: Iterable[Optional[float]]) -> Optional[float]:
    """Nota do pilar = média do Top 2 Box dos itens do pilar (0–100)."""
    valores = [v for v in top2box_por_item if v is not None]
    if not valores:
        return None
    return round(sum(valores) / len(valores), 1)


def calcular_medidor(notas_pilares: dict) -> Optional[float]:
    """Média ponderada dos três pilares, pesos iguais (1/3 cada)."""
    notas = [v for v in notas_pilares.values() if v is not None]
    if len(notas) < 3:
        # Se algum pilar não tem dados, não dá pra fechar o índice geral
        return None
    return round(sum(notas) / 3, 1)


def gate_acionado(notas_pilares: dict) -> list[str]:
    """Retorna lista de pilares cuja nota < 60 — pilares que travam o conjunto."""
    return [p for p, v in notas_pilares.items() if v is not None and v < 60]


# ─── Coletas a partir do banco ─────────────────────────────────────────────

def _respostas_likert_por_item(db: Session, rodada_id: int, tipo: str) -> dict[int, list[int]]:
    """tipo: 'colab' | 'socio'. Retorna {item_numero: [valores]}."""
    ids_query = (
        db.query(RespondenteColab.id).filter(RespondenteColab.rodada_id == rodada_id)
        if tipo == "colab"
        else db.query(RespondenteSocio.id).filter(RespondenteSocio.rodada_id == rodada_id)
    )
    ids = [r[0] for r in ids_query.all()]
    if not ids:
        return {}
    rows = (
        db.query(Resposta.item_numero, Resposta.valor_likert)
        .filter(
            Resposta.tipo_respondente == tipo,
            Resposta.respondente_id.in_(ids),
        )
        .all()
    )
    agrupado: dict[int, list[int]] = defaultdict(list)
    for item_num, valor in rows:
        agrupado[item_num].append(valor)
    return agrupado


def _ancoras(db: Session, rodada_id: int, tipo: str) -> list[int]:
    ids_query = (
        db.query(RespondenteColab.id).filter(RespondenteColab.rodada_id == rodada_id)
        if tipo == "colab"
        else db.query(RespondenteSocio.id).filter(RespondenteSocio.rodada_id == rodada_id)
    )
    ids = [r[0] for r in ids_query.all()]
    if not ids:
        return []
    rows = (
        db.query(RespostaAncora.valor)
        .filter(
            RespostaAncora.tipo_respondente == tipo,
            RespostaAncora.respondente_id.in_(ids),
        )
        .all()
    )
    return [r[0] for r in rows]


# ─── Agregações por pilar (Colaborador) ────────────────────────────────────

def _itens_por_pilar_colab(pilar: str) -> list[int]:
    return [i[0] for i in ITENS_COLABORADOR if i[1] == pilar]


def _itens_por_pilar_socio_espelho(pilar: str) -> list[int]:
    return [i[0] for i in ITENS_SOCIO_ESPELHO if i[1] == pilar]


def _itens_por_pilar_socio_divergente(pilar: str) -> list[int]:
    return [i[0] for i in ITENS_SOCIO_DIVERGENTE if i[1] == pilar]


def calcular_pilares_colab(respostas_por_item: dict[int, list[int]]) -> dict:
    """Para cada pilar Colab, retorna top2/média/distribuição por item + agregados do pilar."""
    resultado = {}
    for pilar in PILARES:
        item_nums = _itens_por_pilar_colab(pilar)
        top2_itens = {}
        media_itens = {}
        dist_itens = {}
        n_itens_resp = {}
        for n in item_nums:
            vals = respostas_por_item.get(n, [])
            top2_itens[n] = calcular_top2box(vals)
            media_itens[n] = calcular_media_ponderada(vals)
            dist_itens[n] = calcular_distribuicao(vals)
            n_itens_resp[n] = len(vals)
        nota_pilar = calcular_nota_pilar(top2_itens.values())
        # Média ponderada do pilar (1-5)
        todas_resp = [v for n in item_nums for v in respostas_por_item.get(n, [])]
        media_pilar = calcular_media_ponderada(todas_resp)
        resultado[pilar] = {
            "top2_por_item": top2_itens,
            "media_por_item": media_itens,
            "distribuicao_por_item": dist_itens,
            "n_por_item": n_itens_resp,
            "nota_pilar": nota_pilar,
            "media_pilar": media_pilar,
            "n_itens": len(item_nums),
            "n_respostas_total": len(todas_resp),
        }
    return resultado


def calcular_pilares_socio_espelho(respostas_por_item: dict[int, list[int]]) -> dict:
    """Mesma estrutura, mas só os 41 itens espelho (1..41)."""
    resultado = {}
    for pilar in PILARES:
        item_nums = _itens_por_pilar_socio_espelho(pilar)
        top2_itens = {}
        media_itens = {}
        for n in item_nums:
            vals = respostas_por_item.get(n, [])
            top2_itens[n] = calcular_top2box(vals)
            media_itens[n] = calcular_media_ponderada(vals)
        nota_pilar = calcular_nota_pilar(top2_itens.values())
        todas_resp = [v for n in item_nums for v in respostas_por_item.get(n, [])]
        media_pilar = calcular_media_ponderada(todas_resp)
        resultado[pilar] = {
            "top2_por_item": top2_itens,
            "media_por_item": media_itens,
            "nota_pilar": nota_pilar,
            "media_pilar": media_pilar,
            "n_itens": len(item_nums),
        }
    return resultado


def calcular_consciencia_sistemica(respostas_por_item: dict[int, list[int]]) -> dict:
    """Índice de Consciência Sistêmica — média Top 2 Box dos 17 divergentes."""
    todos_itens = [i[0] for i in ITENS_SOCIO_DIVERGENTE]
    top2 = []
    media_por_item = {}
    pontos_cegos = []  # itens com nota média 1 ou 2
    for n, pilar, sub, texto in ITENS_SOCIO_DIVERGENTE:
        vals = respostas_por_item.get(n, [])
        t2 = calcular_top2box(vals)
        m = calcular_media_ponderada(vals)
        if t2 is not None:
            top2.append(t2)
        media_por_item[n] = {"top2": t2, "media": m, "pilar": pilar, "subpilar": sub, "texto": texto}
        if m is not None and m <= 2.0:
            pontos_cegos.append({"num": n, "texto": texto, "media": m, "pilar": pilar})

    indice = round(sum(top2) / len(top2), 1) if top2 else None

    # Subpilares (cultura/educação/feedback)
    por_subpilar = {}
    for pilar in PILARES:
        item_nums = _itens_por_pilar_socio_divergente(pilar)
        vals_pilar = []
        for n in item_nums:
            vals = respostas_por_item.get(n, [])
            t2 = calcular_top2box(vals)
            if t2 is not None:
                vals_pilar.append(t2)
        por_subpilar[pilar] = round(sum(vals_pilar) / len(vals_pilar), 1) if vals_pilar else None

    return {
        "indice": indice,
        "por_pilar": por_subpilar,
        "por_item": media_por_item,
        "pontos_cegos": sorted(pontos_cegos, key=lambda x: x["media"]),
    }


# ─── Gap Sócio vs Colaborador ──────────────────────────────────────────────

def calcular_gap_por_item(
    pilares_colab: dict, pilares_socio_espelho: dict
) -> list[dict]:
    """Para cada um dos 41 itens espelho, calcular gap = Top2(Sócio) − Top2(Colab).

    Categorias (§12.1):
    - cegueira_dono: Sócio > Colab em 15+
    - alinhamento: ±14
    - subestimacao: Colab > Sócio em 15+
    """
    saida = []
    for num, pilar, sub, texto_socio, mirror_num in ITENS_SOCIO_ESPELHO:
        t2_socio = pilares_socio_espelho[pilar]["top2_por_item"].get(num)
        t2_colab = pilares_colab[pilar]["top2_por_item"].get(mirror_num)
        if t2_socio is None or t2_colab is None:
            categoria = "sem_dados"
            gap = None
        else:
            gap = round(t2_socio - t2_colab, 1)
            if gap >= 15:
                categoria = "cegueira_dono"
            elif gap <= -15:
                categoria = "subestimacao"
            else:
                categoria = "alinhamento"
        # Texto do colaborador
        texto_colab = next(
            (i[3] for i in ITENS_COLABORADOR if i[0] == mirror_num),
            "",
        )
        saida.append({
            "num_socio": num,
            "num_colab": mirror_num,
            "pilar": pilar,
            "subpilar": sub,
            "texto_socio": texto_socio,
            "texto_colab": texto_colab,
            "top2_socio": t2_socio,
            "top2_colab": t2_colab,
            "gap": gap,
            "categoria": categoria,
        })
    return saida


def consolidar_gap_por_pilar(gaps: list[dict]) -> dict:
    """Para cada pilar: contagem por categoria + top 3 maiores gaps."""
    resultado = {}
    for pilar in PILARES:
        do_pilar = [g for g in gaps if g["pilar"] == pilar]
        cegos = [g for g in do_pilar if g["categoria"] == "cegueira_dono"]
        alinhados = [g for g in do_pilar if g["categoria"] == "alinhamento"]
        subest = [g for g in do_pilar if g["categoria"] == "subestimacao"]
        sem_dados = [g for g in do_pilar if g["categoria"] == "sem_dados"]
        # Top 3 maiores gaps positivos (cegueira)
        com_gap = [g for g in do_pilar if g["gap"] is not None]
        top_3_cegueira = sorted(
            com_gap, key=lambda x: x["gap"], reverse=True
        )[:3]
        resultado[pilar] = {
            "n_cegueira": len(cegos),
            "n_alinhamento": len(alinhados),
            "n_subestimacao": len(subest),
            "n_sem_dados": len(sem_dados),
            "top_3_cegueira": top_3_cegueira,
            "itens": sorted(do_pilar, key=lambda x: (x["gap"] if x["gap"] is not None else -999), reverse=True),
        }
    return resultado


# ─── Cortes demográficos ───────────────────────────────────────────────────

def cortes_demograficos(
    db: Session,
    rodada_id: int,
) -> dict:
    """Calcula nota dos três pilares + Medidor para cada segmento demográfico.

    Segmentos com < MINIMO_PARA_REPORTAR_CORTE respondentes são SUPRIMIDOS.
    """
    respondentes = (
        db.query(RespondenteColab)
        .filter(RespondenteColab.rodada_id == rodada_id)
        .all()
    )
    # Mapa respondente_id → respostas Likert
    resp_ids = [r.id for r in respondentes]
    if not resp_ids:
        return {"tempo_de_casa": {}, "tipo_de_cargo": {}, "area": {}}

    rows = (
        db.query(Resposta.respondente_id, Resposta.item_numero, Resposta.valor_likert)
        .filter(
            Resposta.tipo_respondente == "colab",
            Resposta.respondente_id.in_(resp_ids),
        )
        .all()
    )
    por_resp: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for rid, item, val in rows:
        por_resp[rid].append((item, val))

    def _calcular_metricas_segmento(ids_segmento: list[int]) -> Optional[dict]:
        if len(ids_segmento) < MINIMO_PARA_REPORTAR_CORTE:
            return None
        respostas_agrupadas: dict[int, list[int]] = defaultdict(list)
        for rid in ids_segmento:
            for item, val in por_resp.get(rid, []):
                respostas_agrupadas[item].append(val)
        pilares = calcular_pilares_colab(respostas_agrupadas)
        notas = {p: pilares[p]["nota_pilar"] for p in PILARES}
        medidor = calcular_medidor(notas)
        return {
            "n_respondentes": len(ids_segmento),
            "notas_pilares": notas,
            "medidor": medidor,
        }

    def _agrupar_por(attr: str) -> dict:
        grupos: dict[str, list[int]] = defaultdict(list)
        for r in respondentes:
            chave = getattr(r, attr) or "_sem_resposta_"
            grupos[chave].append(r.id)
        saida = {}
        for chave, ids in grupos.items():
            n = len(ids)
            metricas = _calcular_metricas_segmento(ids)
            saida[chave] = {
                "n_respondentes": n,
                "suprimido": metricas is None,
                "motivo_supressao": (
                    f"Apenas {n} respondente(s) — abaixo do mínimo de {MINIMO_PARA_REPORTAR_CORTE} para preservar anonimato."
                    if metricas is None else None
                ),
                "metricas": metricas,
            }
        return saida

    return {
        "tempo_de_casa": _agrupar_por("tempo_de_casa"),
        "tipo_de_cargo": _agrupar_por("tipo_de_cargo"),
        "area": _agrupar_por("area"),
    }


# ─── Função orquestradora completa ─────────────────────────────────────────

def calcular_relatorio_completo(db: Session, rodada_id: int) -> dict:
    """Computa todas as métricas necessárias para o relatório de uma rodada."""
    rodada = db.query(Rodada).filter(Rodada.id == rodada_id).first()
    if rodada is None:
        raise ValueError(f"Rodada {rodada_id} não encontrada")

    # Counts
    n_colab = (
        db.query(RespondenteColab)
        .filter(RespondenteColab.rodada_id == rodada_id)
        .count()
    )
    n_socio = (
        db.query(RespondenteSocio)
        .filter(RespondenteSocio.rodada_id == rodada_id)
        .count()
    )

    # Respostas Likert
    respostas_colab = _respostas_likert_por_item(db, rodada_id, "colab")
    respostas_socio = _respostas_likert_por_item(db, rodada_id, "socio")

    # Pilares (colab) — base do Medidor
    pilares_colab = calcular_pilares_colab(respostas_colab)
    notas_pilares_colab = {p: pilares_colab[p]["nota_pilar"] for p in PILARES}
    medidor = calcular_medidor(notas_pilares_colab)
    pilares_travados = gate_acionado(notas_pilares_colab)

    # Pilares (sócio) — só itens espelho
    pilares_socio_espelho = calcular_pilares_socio_espelho(respostas_socio)
    notas_pilares_socio = {p: pilares_socio_espelho[p]["nota_pilar"] for p in PILARES}

    # Gap
    gaps = calcular_gap_por_item(pilares_colab, pilares_socio_espelho)
    gaps_consolidados = consolidar_gap_por_pilar(gaps)

    # Consciência sistêmica (divergentes)
    consciencia = calcular_consciencia_sistemica(respostas_socio)

    # Âncoras
    ancoras_colab = _ancoras(db, rodada_id, "colab")
    ancoras_socio = _ancoras(db, rodada_id, "socio")
    ancora_colab_t2 = calcular_top2box(ancoras_colab)
    ancora_colab_media = calcular_media_ponderada(ancoras_colab)
    ancora_socio_t2 = calcular_top2box(ancoras_socio)
    ancora_socio_media = calcular_media_ponderada(ancoras_socio)

    # NPS
    nps_ids = [r.id for r in db.query(RespondenteColab).filter(RespondenteColab.rodada_id == rodada_id).all()]
    if nps_ids:
        nps_vals = [r[0] for r in db.query(RespostaNPS.valor_0_10).filter(RespostaNPS.respondente_id.in_(nps_ids)).all()]
    else:
        nps_vals = []
    enps = calcular_enps(nps_vals)

    # Retenção
    if nps_ids:
        ret_rows = (
            db.query(RespostaRetencao.opcao_escolhida, RespostaRetencao.texto_aberto)
            .filter(RespostaRetencao.respondente_id.in_(nps_ids))
            .all()
        )
    else:
        ret_rows = []
    cont = Counter(r[0] for r in ret_rows)
    total_ret = sum(cont.values())
    retencao = {
        "total": total_ret,
        "distribuicao": {
            opcao: {
                "n": n,
                "pct": round(n / total_ret * 100, 1) if total_ret else 0,
            }
            for opcao, n in cont.items()
        },
        "textos_abertos": [t for _, t in ret_rows if t],
    }

    # Cortes demográficos
    cortes = cortes_demograficos(db, rodada_id)

    # Comparação com rodada anterior (se houver)
    comparacao = comparar_com_anterior(db, rodada_id)

    # Faixa do medidor
    faixa = faixa_do_medidor(medidor) if medidor is not None else faixa_do_medidor(0)

    return {
        "rodada": {
            "id": rodada.id,
            "tipo": rodada.tipo,
            "data_inicio": rodada.data_inicio,
            "data_fim": rodada.data_fim,
            "status": rodada.status,
        },
        "empresa": {
            "id": rodada.empresa.id,
            "nome": rodada.empresa.nome,
        },
        "contagens": {
            "colaboradores": n_colab,
            "socios": n_socio,
            "total": n_colab + n_socio,
        },
        "medidor": medidor,
        "faixa": faixa,
        "pilares_colab": pilares_colab,
        "notas_pilares_colab": notas_pilares_colab,
        "pilares_travados": pilares_travados,  # gate visual §11.5
        "gate_acionado": len(pilares_travados) > 0,
        "pilares_socio_espelho": pilares_socio_espelho,
        "notas_pilares_socio": notas_pilares_socio,
        "gaps": gaps,
        "gaps_consolidados": gaps_consolidados,
        "consciencia": consciencia,
        "ancora": {
            "colab": {"top2": ancora_colab_t2, "media": ancora_colab_media, "n": len(ancoras_colab)},
            "socio": {"top2": ancora_socio_t2, "media": ancora_socio_media, "n": len(ancoras_socio)},
            "gap": (
                round(ancora_socio_t2 - ancora_colab_t2, 1)
                if (ancora_socio_t2 is not None and ancora_colab_t2 is not None)
                else None
            ),
        },
        "enps": enps,
        "retencao": retencao,
        "cortes": cortes,
        "comparacao": comparacao,
    }
