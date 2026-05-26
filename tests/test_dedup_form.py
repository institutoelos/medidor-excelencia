"""Teste de dedup do formulário via cookie."""
import importlib
import pytest


@pytest.fixture
def setup_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_dedup.db"
    monkeypatch.setenv("MEDIDOR_DB_PATH", str(db_file))
    # Reset módulos para usar novo DB
    import app.models.db as dbmod
    importlib.reload(dbmod)
    import app.services.engine as engine_mod
    importlib.reload(engine_mod)
    import app.services.qr as qrmod  # noqa
    import app.routers.forms as forms_mod
    importlib.reload(forms_mod)
    import app.routers.admin as admin_mod
    importlib.reload(admin_mod)
    import app.routers.report as report_mod
    importlib.reload(report_mod)
    import app.main as mainmod
    importlib.reload(mainmod)

    dbmod.init_db()
    # Cria empresa+rodada+token
    s = dbmod.SessionLocal()
    emp = dbmod.Empresa(nome="Empresa Dedup", lista_de_areas="ti")
    s.add(emp); s.commit(); s.refresh(emp)
    rod = dbmod.Rodada(empresa_id=emp.id, tipo="entrada")
    s.add(rod); s.commit(); s.refresh(rod)
    token_colab = rod.token_colab
    s.close()

    from fastapi.testclient import TestClient
    return TestClient(mainmod.app), token_colab


def _submit_colab(client, token):
    data = {
        "ancora": "4",
        "nps": "9",
        "retencao": "proposito",
        "tempo_de_casa": "1_3a",
        "tipo_de_cargo": "colaborador",
        "area": "ti",
    }
    for n in range(1, 59):
        data[f"item_{n}"] = "4"
    return client.post(f"/f/colab/{token}/enviar", data=data, follow_redirects=False)


def test_primeiro_envio_seta_cookie(setup_db):
    client, token = setup_db
    r = _submit_colab(client, token)
    assert r.status_code == 303
    # Cookie deve aparecer
    cookies = r.cookies
    assert any(k.startswith("med_colab_") for k in cookies.keys())


def test_segundo_get_no_mesmo_navegador_mostra_obrigado(setup_db):
    client, token = setup_db
    r1 = _submit_colab(client, token)
    assert r1.status_code == 303
    # GET no formulário com cookie deve render "obrigado" (não o form longo)
    r2 = client.get(f"/f/colab/{token}")
    assert r2.status_code == 200
    assert "Obrigado" in r2.text
    assert "name=\"item_1\"" not in r2.text


def test_segundo_post_redireciona_sem_duplicar(setup_db):
    client, token = setup_db
    r1 = _submit_colab(client, token)
    assert r1.status_code == 303
    # Tenta postar de novo no mesmo cliente (mantém cookie)
    r2 = _submit_colab(client, token)
    assert r2.status_code == 303
    # DB só deve ter 1 respondente
    import app.models.db as dbmod
    s = dbmod.SessionLocal()
    n = s.query(dbmod.RespondenteColab).count()
    s.close()
    assert n == 1


def test_navegador_sem_cookie_renderiza_form_normalmente(setup_db):
    client, token = setup_db
    _submit_colab(client, token)
    # Cliente novo (sem cookie)
    from fastapi.testclient import TestClient
    import app.main as mainmod
    novo = TestClient(mainmod.app)
    r = novo.get(f"/f/colab/{token}")
    assert r.status_code == 200
    assert "item_1" in r.text  # form de verdade
