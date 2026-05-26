"""Testes unitários da engine de cálculo — princípios não negociáveis §17."""
import pytest

from app.services.engine import (
    calcular_enps,
    calcular_gap_por_item,
    calcular_medidor,
    calcular_media_ponderada,
    calcular_nota_pilar,
    calcular_pilares_colab,
    calcular_pilares_socio_espelho,
    calcular_top2box,
    gate_acionado,
    MINIMO_PARA_REPORTAR_CORTE,
)
from app.content.items import PILAR_CULTURA, PILAR_EDUCACAO, PILAR_FEEDBACK, PILARES


# ─── Top 2 Box e Média ─────────────────────────────────────────────────────

def test_top2box_basico():
    # 3 de 5 marcaram 4 ou 5 → 60.0
    assert calcular_top2box([5, 4, 3, 4, 1]) == 60.0


def test_top2box_todos_topo():
    assert calcular_top2box([5, 5, 5, 5]) == 100.0


def test_top2box_zero():
    assert calcular_top2box([1, 2, 3]) == 0.0


def test_top2box_vazio_retorna_none():
    assert calcular_top2box([]) is None


def test_media_ponderada():
    assert calcular_media_ponderada([5, 4, 3, 2, 1]) == 3.0


def test_media_ponderada_vazio_none():
    assert calcular_media_ponderada([]) is None


# ─── eNPS (princípio não negociável #1) ────────────────────────────────────

def test_enps_todos_promotores_eh_100():
    r = calcular_enps([10, 10, 9, 9, 10])
    assert r["enps"] == 100.0
    assert r["promotores"] == 5
    assert r["detratores"] == 0


def test_enps_todos_detratores_eh_menos_100():
    r = calcular_enps([0, 3, 6, 5, 2])
    assert r["enps"] == -100.0
    assert r["detratores"] == 5
    assert r["promotores"] == 0


def test_enps_mix_balanceado():
    # 4 promotores (40%), 4 detratores (40%), 2 neutros (20%) → eNPS = 0
    r = calcular_enps([10, 9, 10, 9, 0, 3, 5, 6, 7, 8])
    assert r["enps"] == 0.0
    assert r["promotores"] == 4
    assert r["detratores"] == 4
    assert r["neutros"] == 2


def test_enps_zero_respondentes_retorna_none():
    r = calcular_enps([])
    assert r["enps"] is None
    assert r["total"] == 0


def test_enps_nao_eh_media_aritmetica():
    """Caso emblemático: média seria 8.0, mas eNPS real é +40."""
    notas = [10, 10, 10, 8, 8]  # 3 promotores, 2 neutros, 0 detratores
    r = calcular_enps(notas)
    assert r["enps"] == 60.0  # 60% promo - 0% detrator
    media_aritmetica = sum(notas) / len(notas)
    assert media_aritmetica == 9.2  # demonstra que nunca confundimos
    assert r["enps"] != media_aritmetica


# ─── Nota por pilar e Medidor ──────────────────────────────────────────────

def test_nota_pilar_eh_media_dos_top2():
    notas = [80.0, 90.0, 70.0]
    assert calcular_nota_pilar(notas) == 80.0


def test_nota_pilar_ignora_none():
    assert calcular_nota_pilar([80.0, None, 60.0]) == 70.0


def test_medidor_pesos_iguais_entre_pilares():
    notas = {PILAR_CULTURA: 60.0, PILAR_EDUCACAO: 90.0, PILAR_FEEDBACK: 75.0}
    # Média simples: 75.0
    assert calcular_medidor(notas) == 75.0


def test_medidor_none_se_falta_pilar():
    assert calcular_medidor({PILAR_CULTURA: 80.0, PILAR_EDUCACAO: 70.0, PILAR_FEEDBACK: None}) is None


# ─── Gate visual (princípio não negociável #4) ─────────────────────────────

def test_gate_aciona_em_pilar_abaixo_60():
    notas = {PILAR_CULTURA: 80.0, PILAR_EDUCACAO: 50.0, PILAR_FEEDBACK: 75.0}
    travados = gate_acionado(notas)
    assert travados == [PILAR_EDUCACAO]


def test_gate_nao_aciona_se_todos_acima_60():
    notas = {PILAR_CULTURA: 80.0, PILAR_EDUCACAO: 70.0, PILAR_FEEDBACK: 65.0}
    assert gate_acionado(notas) == []


def test_gate_nao_altera_medidor():
    """Não negociável: gate é visual, NÃO matemático."""
    notas = {PILAR_CULTURA: 80.0, PILAR_EDUCACAO: 30.0, PILAR_FEEDBACK: 70.0}
    medidor_pre_gate = calcular_medidor(notas)
    travados = gate_acionado(notas)
    # Mesmo com gate ativo, o medidor é a média pura
    assert medidor_pre_gate == 60.0  # (80+30+70)/3
    assert PILAR_EDUCACAO in travados
    # Confirma que não há nenhum side-effect que mude o número
    medidor_pos_gate = calcular_medidor(notas)
    assert medidor_pos_gate == medidor_pre_gate


# ─── Pilares (Colaborador) ──────────────────────────────────────────────────

def _respostas_colab_todas_4(item_nums):
    """Helper: para uma lista de números de item, devolve {n: [4,4,4]}."""
    return {n: [4, 4, 4] for n in item_nums}


def test_pilares_colab_todos_4_resulta_em_100_top2():
    from app.content.items import ITENS_COLABORADOR
    nums = [i[0] for i in ITENS_COLABORADOR]
    respostas = _respostas_colab_todas_4(nums)
    pilares = calcular_pilares_colab(respostas)
    for p in PILARES:
        assert pilares[p]["nota_pilar"] == 100.0
        assert pilares[p]["media_pilar"] == 4.0


def test_pilares_colab_metade_4_metade_3():
    from app.content.items import ITENS_COLABORADOR
    nums = [i[0] for i in ITENS_COLABORADOR]
    respostas = {n: [4, 4, 3, 3] for n in nums}
    pilares = calcular_pilares_colab(respostas)
    for p in PILARES:
        # 50% top 2 box em cada item → nota pilar = 50.0
        assert pilares[p]["nota_pilar"] == 50.0


# ─── Gap por item espelho ──────────────────────────────────────────────────

def test_gap_categorias():
    from app.content.items import ITENS_COLABORADOR, ITENS_SOCIO_ESPELHO
    # Forçar diferenças conhecidas
    nums_colab = [i[0] for i in ITENS_COLABORADOR]
    nums_socio_esp = [i[0] for i in ITENS_SOCIO_ESPELHO]

    respostas_colab = {n: [3] * 10 for n in nums_colab}  # Top2 = 0
    respostas_socio = {n: [5] * 10 for n in nums_socio_esp}  # Top2 = 100
    pc = calcular_pilares_colab(respostas_colab)
    ps = calcular_pilares_socio_espelho(respostas_socio)
    gaps = calcular_gap_por_item(pc, ps)
    assert all(g["gap"] == 100.0 for g in gaps)
    assert all(g["categoria"] == "cegueira_dono" for g in gaps)


def test_gap_alinhamento():
    from app.content.items import ITENS_COLABORADOR, ITENS_SOCIO_ESPELHO
    nums_colab = [i[0] for i in ITENS_COLABORADOR]
    nums_socio_esp = [i[0] for i in ITENS_SOCIO_ESPELHO]
    respostas_colab = {n: [4, 5, 4] for n in nums_colab}  # Top2 = 100
    respostas_socio = {n: [4, 5, 4] for n in nums_socio_esp}  # Top2 = 100
    pc = calcular_pilares_colab(respostas_colab)
    ps = calcular_pilares_socio_espelho(respostas_socio)
    gaps = calcular_gap_por_item(pc, ps)
    assert all(g["gap"] == 0.0 for g in gaps)
    assert all(g["categoria"] == "alinhamento" for g in gaps)


def test_gap_subestimacao():
    from app.content.items import ITENS_COLABORADOR, ITENS_SOCIO_ESPELHO
    nums_colab = [i[0] for i in ITENS_COLABORADOR]
    nums_socio_esp = [i[0] for i in ITENS_SOCIO_ESPELHO]
    respostas_colab = {n: [5] * 10 for n in nums_colab}  # Top2 = 100
    respostas_socio = {n: [2] * 10 for n in nums_socio_esp}  # Top2 = 0
    pc = calcular_pilares_colab(respostas_colab)
    ps = calcular_pilares_socio_espelho(respostas_socio)
    gaps = calcular_gap_por_item(pc, ps)
    assert all(g["gap"] == -100.0 for g in gaps)
    assert all(g["categoria"] == "subestimacao" for g in gaps)


# ─── Regra de 5+ respondentes (princípio não negociável #2) ────────────────

def test_constante_minimo_eh_5():
    assert MINIMO_PARA_REPORTAR_CORTE == 5


def test_cortes_5_mais_respondentes_funciona_e_2e_um_suprime(tmp_path, monkeypatch):
    """Teste integrado leve: insere 5 colab num segmento e 2 em outro."""
    db_file = tmp_path / "test_engine.db"
    monkeypatch.setenv("MEDIDOR_DB_PATH", str(db_file))
    # Importar depois de setar env var
    import importlib
    import app.models.db as dbmod
    importlib.reload(dbmod)
    import app.services.engine as engine_mod
    importlib.reload(engine_mod)

    dbmod.init_db()
    s = dbmod.SessionLocal()
    emp = dbmod.Empresa(nome="Teste Cortes")
    s.add(emp); s.commit(); s.refresh(emp)
    rod = dbmod.Rodada(empresa_id=emp.id, tipo="entrada")
    s.add(rod); s.commit(); s.refresh(rod)

    from app.content.items import ITENS_COLABORADOR
    nums = [i[0] for i in ITENS_COLABORADOR]

    def add_respondente(tempo, cargo, area):
        r = dbmod.RespondenteColab(rodada_id=rod.id, tempo_de_casa=tempo, tipo_de_cargo=cargo, area=area)
        s.add(r); s.commit(); s.refresh(r)
        for n in nums:
            s.add(dbmod.Resposta(respondente_id=r.id, tipo_respondente="colab", item_numero=n, valor_likert=4))
        s.commit()
        return r

    for _ in range(5):
        add_respondente("ate_6m", "colaborador", "vendas")
    for _ in range(2):
        add_respondente("mais_5a", "colaborador", "engenharia")

    cortes = engine_mod.cortes_demograficos(s, rod.id)
    # vendas tem 5+, engenharia tem 2 (deve ser suprimido)
    assert cortes["area"]["vendas"]["suprimido"] is False
    assert cortes["area"]["engenharia"]["suprimido"] is True
    assert cortes["area"]["engenharia"]["metricas"] is None

    s.close()
