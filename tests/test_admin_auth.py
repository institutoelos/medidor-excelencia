"""Smoke test do login admin via HTTPBasic."""
import base64

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def _basic(user: str, pwd: str) -> dict:
    cred = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    return {"Authorization": f"Basic {cred}"}


def test_admin_sem_auth_eh_401(client):
    r = client.get("/admin")
    assert r.status_code == 401
    assert "WWW-Authenticate" in r.headers


def test_admin_auth_errada_eh_401(client):
    r = client.get("/admin", headers=_basic("admin", "errado"))
    assert r.status_code == 401


def test_admin_auth_ok_eh_200(client):
    r = client.get("/admin", headers=_basic("admin", "elos"))
    assert r.status_code == 200


def test_formulario_publico_nao_pede_auth(client):
    # 404 porque token inexistente, mas não 401
    r = client.get("/f/colab/token-inexistente")
    assert r.status_code in (404,)
    r = client.get("/f/socio/token-inexistente")
    assert r.status_code in (404,)


def test_relatorio_publico_nao_pede_auth(client):
    r = client.get("/relatorio/99999")
    assert r.status_code in (404,)
