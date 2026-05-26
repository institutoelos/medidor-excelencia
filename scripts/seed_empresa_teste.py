"""Popula o banco com a Empresa Teste S.A. — 45 colaboradores + 2 sócios.

Cria 2 cenários por sócio (com e sem gate) para validar gate visual.
A distribuição demográfica garante segmentos com 5+ e segmentos com <5
(para validar regra de supressão).

Rodar: python scripts/seed_empresa_teste.py
"""
from __future__ import annotations

import os
import random
import sys

# Permite rodar como script direto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.content.items import (
    ITENS_COLABORADOR,
    ITENS_SOCIO_DIVERGENTE,
    ITENS_SOCIO_ESPELHO,
    PILAR_CULTURA,
    PILAR_EDUCACAO,
    PILAR_FEEDBACK,
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
    SessionLocal,
    init_db,
)

random.seed(42)


# ─── Cenário ───────────────────────────────────────────────────────────────
# 45 colaboradores distribuídos para que:
# - "vendas" tenha 12 (reportável)
# - "operacoes" tenha 14 (reportável)
# - "financeiro" tenha 11 (reportável)
# - "engenharia" tenha 3 (suprimido por regra de 5+)
# - "rh" tenha 5 (reportável no limite)
# Cargos: ~6 liderança sênior, ~10 intermediária, ~25 colaborador, ~4 estagiário
# Tempo de casa misturado em 5 faixas

DISTRIBUICAO = [
    # (area, cargo, tempo, qtd, perfil_resposta)
    ("vendas", "lid_senior", "mais_5a", 2, "alto"),
    ("vendas", "lid_intermediaria", "3_5a", 3, "alto"),
    ("vendas", "colaborador", "1_3a", 5, "alto"),
    ("vendas", "colaborador", "6m_1a", 2, "medio"),

    ("operacoes", "lid_senior", "mais_5a", 1, "alto"),
    ("operacoes", "lid_intermediaria", "3_5a", 3, "alto"),
    ("operacoes", "colaborador", "1_3a", 6, "medio"),
    ("operacoes", "colaborador", "ate_6m", 4, "alto"),

    ("financeiro", "lid_senior", "3_5a", 2, "alto"),
    ("financeiro", "lid_intermediaria", "1_3a", 2, "alto"),
    ("financeiro", "colaborador", "1_3a", 4, "medio"),
    ("financeiro", "colaborador", "ate_6m", 3, "alto"),

    ("rh", "lid_senior", "mais_5a", 1, "alto"),
    ("rh", "lid_intermediaria", "3_5a", 1, "alto"),
    ("rh", "colaborador", "1_3a", 3, "medio"),

    # área que será suprimida (apenas 3) — valida regra de 5+
    ("engenharia", "estagiario", "ate_6m", 3, "medio"),
]


def perfil_likert(perfil: str, pilar: str) -> int:
    """Devolve um valor 1-5 de acordo com o perfil e pilar."""
    def amostra(probs):
        r = random.random()
        acc = 0
        for v, p in probs:
            acc += p
            if r <= acc:
                return v
        return probs[-1][0]

    if perfil == "alto":
        return amostra([(5, 0.45), (4, 0.35), (3, 0.15), (2, 0.04), (1, 0.01)])
    if perfil == "medio":
        return amostra([(5, 0.20), (4, 0.35), (3, 0.30), (2, 0.10), (1, 0.05)])
    if perfil == "medio_baixo":
        return amostra([(5, 0.08), (4, 0.22), (3, 0.40), (2, 0.20), (1, 0.10)])
    if perfil == "baixo_feedback":
        # cultura/educacao razoáveis, feedback ruim
        if pilar == PILAR_FEEDBACK:
            return amostra([(5, 0.03), (4, 0.10), (3, 0.25), (2, 0.35), (1, 0.27)])
        return amostra([(5, 0.15), (4, 0.30), (3, 0.30), (2, 0.15), (1, 0.10)])
    return amostra([(5, 0.2), (4, 0.3), (3, 0.3), (2, 0.15), (1, 0.05)])


def perfil_nps(perfil: str) -> int:
    if perfil == "alto":
        return random.choices([10, 9, 8, 7, 6, 5, 4, 3], [0.4, 0.3, 0.15, 0.08, 0.04, 0.02, 0.01, 0.0])[0]
    if perfil == "medio":
        return random.choices([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [0.15, 0.20, 0.20, 0.15, 0.10, 0.08, 0.05, 0.04, 0.02, 0.005, 0.005])[0]
    if perfil == "medio_baixo":
        return random.choices([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [0.05, 0.10, 0.15, 0.10, 0.15, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03])[0]
    if perfil == "baixo_feedback":
        return random.choices([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [0.05, 0.10, 0.10, 0.10, 0.20, 0.15, 0.10, 0.08, 0.06, 0.04, 0.02])[0]
    return random.randint(0, 10)


def perfil_retencao(perfil: str) -> str:
    if perfil == "alto":
        return random.choice(["proposito", "vinculo", "valores", "crescimento", "crescimento"])
    if perfil == "baixo_feedback":
        return random.choice(["seguranca", "remuneracao", "vinculo"])
    return random.choice(["crescimento", "proposito", "vinculo", "remuneracao", "seguranca", "valores"])


def gerar_empresa_teste(rotulo: str = "Empresa Teste S.A.", gate_ativo: bool = False) -> int:
    """Cria empresa + rodada de entrada + 45 colaboradores + 2 sócios.

    Se gate_ativo=True, força o pilar Feedback a cair abaixo de 60.
    """
    init_db()
    s = SessionLocal()
    try:
        empresa = Empresa(
            nome=rotulo,
            lista_de_areas="vendas, operacoes, financeiro, rh, engenharia",
        )
        s.add(empresa); s.commit(); s.refresh(empresa)

        rodada = Rodada(empresa_id=empresa.id, tipo="entrada")
        s.add(rodada); s.commit(); s.refresh(rodada)

        # Colaboradores
        for area, cargo, tempo, qtd, perfil_base in DISTRIBUICAO:
            for _ in range(qtd):
                perfil = perfil_base
                # Se gate_ativo, agrava feedback geral
                if gate_ativo and perfil not in ("baixo_feedback",):
                    perfil_pilar = lambda pilar, p=perfil: (
                        random.choices([1, 2, 3], [0.40, 0.40, 0.20])[0] if pilar == PILAR_FEEDBACK
                        else perfil_likert(p, pilar)
                    )
                else:
                    perfil_pilar = lambda pilar, p=perfil: perfil_likert(p, pilar)

                r = RespondenteColab(
                    rodada_id=rodada.id,
                    tempo_de_casa=tempo,
                    tipo_de_cargo=cargo,
                    area=area,
                )
                s.add(r); s.flush()
                for num, pilar, sub, texto in ITENS_COLABORADOR:
                    valor = perfil_pilar(pilar)
                    s.add(Resposta(respondente_id=r.id, tipo_respondente="colab", item_numero=num, valor_likert=valor))
                s.add(RespostaAncora(respondente_id=r.id, tipo_respondente="colab", valor=perfil_pilar(PILAR_CULTURA)))
                s.add(RespostaNPS(respondente_id=r.id, valor_0_10=perfil_nps(perfil)))
                s.add(RespostaRetencao(respondente_id=r.id, opcao_escolhida=perfil_retencao(perfil)))
                # marca como finalizado
                from datetime import datetime
                r.finalizado_em = datetime.utcnow()
        s.commit()

        # Sócios (2). Geramos uma percepção sócio bem alta (gera "cegueira do dono" forte no relatório)
        for socio_perfil in ["socio_otimista", "socio_otimista"]:
            soc = RespondenteSocio(rodada_id=rodada.id)
            s.add(soc); s.flush()
            # espelho — alto
            for num, pilar, sub, texto, mirror in ITENS_SOCIO_ESPELHO:
                valor = random.choices([5, 4, 3, 2, 1], [0.55, 0.30, 0.10, 0.04, 0.01])[0]
                s.add(Resposta(respondente_id=soc.id, tipo_respondente="socio", item_numero=num, valor_likert=valor))
            # divergentes — mistura: sócio tem consciência média
            for num, pilar, sub, texto in ITENS_SOCIO_DIVERGENTE:
                valor = random.choices([5, 4, 3, 2, 1], [0.20, 0.30, 0.30, 0.15, 0.05])[0]
                s.add(Resposta(respondente_id=soc.id, tipo_respondente="socio", item_numero=num, valor_likert=valor))
            s.add(RespostaAncora(respondente_id=soc.id, tipo_respondente="socio", valor=5))
            from datetime import datetime
            soc.finalizado_em = datetime.utcnow()
        s.commit()

        print(f"✓ Empresa criada: id={empresa.id} '{empresa.nome}' (gate_ativo={gate_ativo})")
        print(f"  Rodada {rodada.tipo} id={rodada.id}")
        print(f"  Link colab: /f/colab/{rodada.token_colab}")
        print(f"  Link sócio: /f/socio/{rodada.token_socio}")
        print(f"  Relatório:  /relatorio/{rodada.id}")
        return rodada.id
    finally:
        s.close()


def main():
    print("Populando cenário Empresa Teste S.A.…")
    # Reset opcional
    if "--reset" in sys.argv:
        from app.models.db import Base, engine
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("  (banco resetado)")
    rid1 = gerar_empresa_teste("Empresa Teste S.A.", gate_ativo=False)
    rid2 = gerar_empresa_teste("Empresa Teste (Gate Ativo)", gate_ativo=True)
    print(f"\n→ Cenário base (sem gate): rodada {rid1}")
    print(f"→ Cenário com gate ativo:   rodada {rid2}")


if __name__ == "__main__":
    main()
