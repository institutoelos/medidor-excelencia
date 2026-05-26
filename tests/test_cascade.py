"""Cascade limpa respostas ao deletar respondente/rodada/empresa (FK polimórfico manual)."""
import importlib
import pytest


@pytest.fixture
def db_iso(tmp_path, monkeypatch):
    db_file = tmp_path / "test_cascade.db"
    monkeypatch.setenv("MEDIDOR_DB_PATH", str(db_file))
    import app.models.db as dbmod
    importlib.reload(dbmod)
    dbmod.init_db()
    return dbmod


def test_deletar_empresa_apaga_respostas(db_iso):
    dbmod = db_iso
    s = dbmod.SessionLocal()
    emp = dbmod.Empresa(nome="X")
    s.add(emp); s.commit(); s.refresh(emp)
    rod = dbmod.Rodada(empresa_id=emp.id, tipo="entrada")
    s.add(rod); s.commit(); s.refresh(rod)
    resp = dbmod.RespondenteColab(rodada_id=rod.id, tempo_de_casa="ate_6m", tipo_de_cargo="colaborador", area="x")
    s.add(resp); s.commit(); s.refresh(resp)
    s.add(dbmod.Resposta(respondente_id=resp.id, tipo_respondente="colab", item_numero=1, valor_likert=4))
    s.add(dbmod.RespostaAncora(respondente_id=resp.id, tipo_respondente="colab", valor=5))
    s.add(dbmod.RespostaNPS(respondente_id=resp.id, valor_0_10=9))
    s.commit()

    assert s.query(dbmod.Resposta).count() == 1
    assert s.query(dbmod.RespostaNPS).count() == 1

    s.delete(emp); s.commit()

    assert s.query(dbmod.RespondenteColab).count() == 0
    assert s.query(dbmod.Resposta).count() == 0, "resposta órfã ficou após delete empresa"
    assert s.query(dbmod.RespostaAncora).count() == 0
    assert s.query(dbmod.RespostaNPS).count() == 0
    s.close()
