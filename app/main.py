"""FastAPI app — Medidor de Excelência ELOS."""
from __future__ import annotations

import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.db import init_db
from app.routers import admin, export, forms, report
from app.services.auth import (
    COOKIE_NAME,
    COOKIE_SECURE,
    MAX_AGE_SEC,
    criar_token_sessao,
    usuario_da_sessao,
    verificar_credenciais,
)

app = FastAPI(title="Medidor de Excelência ELOS — Pilar Pessoas")

_BASE = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(_BASE, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(_BASE, "templates"))

app.include_router(forms.router)
app.include_router(admin.router)
app.include_router(export.router)
app.include_router(report.router)


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Browsers legacy/diretos buscam /favicon.ico sem ler o <link rel='icon'>."""
    return RedirectResponse("/static/img/signo-elos.png", status_code=301)


@app.get("/healthz")
def healthz():
    return {
        "sistema": "Medidor de Excelência ELOS — Pilar Pessoas",
        "versao": "1.1",
        "status": "ok",
        "rotas": {
            "admin": "/admin (requer login)",
            "formulario_colaborador": "/f/colab/{token}",
            "formulario_socio": "/f/socio/{token}",
            "relatorio": "/relatorio/{rodada_id}",
        },
    }


def _safe_next(value: str | None) -> str:
    # Aceita só paths internos (evita open redirect via ?next=).
    if not value or not value.startswith("/") or value.startswith("//"):
        return "/admin"
    return value


@app.get("/login")
def login_form(request: Request, next: str = "/admin", erro: int = 0):
    destino = _safe_next(next)
    if usuario_da_sessao(request.cookies.get(COOKIE_NAME)):
        return RedirectResponse(destino, status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "next": destino, "erro": bool(erro)},
    )


@app.post("/login")
def login_submit(
    usuario: str = Form(...),
    senha: str = Form(...),
    next: str = Form("/admin"),
):
    destino = _safe_next(next)
    if not verificar_credenciais(usuario, senha):
        return RedirectResponse(f"/login?erro=1&next={destino}", status_code=303)
    resp = RedirectResponse(destino, status_code=303)
    resp.set_cookie(
        COOKIE_NAME,
        criar_token_sessao(usuario),
        max_age=MAX_AGE_SEC,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
    )
    return resp


@app.get("/logout")
def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie(COOKIE_NAME)
    return resp
