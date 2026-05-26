"""FastAPI app — Medidor de Excelência ELOS."""
from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.db import init_db
from app.routers import admin, export, forms, report

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
