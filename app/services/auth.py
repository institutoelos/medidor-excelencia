"""Autenticação do painel admin via sessão assinada em cookie.

Credenciais vêm das variáveis MEDIDOR_ADMIN_USER e MEDIDOR_ADMIN_PASSWORD
(default: admin / elos). O cookie de sessão é assinado com MEDIDOR_SESSION_SECRET;
se a variável não estiver definida, o secret é derivado da senha — assim, trocar
a senha invalida sessões antigas automaticamente.
"""
from __future__ import annotations

import os
import secrets
from typing import Optional

from fastapi import HTTPException, Request, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

_ADMIN_USER = os.environ.get("MEDIDOR_ADMIN_USER", "admin")
_ADMIN_PASSWORD = os.environ.get("MEDIDOR_ADMIN_PASSWORD", "elos")

# Em produção (Railway define RAILWAY_ENVIRONMENT_NAME ou similar), recusa subir
# com senha default. Bypass com MEDIDOR_ALLOW_DEFAULT_PASSWORD=1 pra testes locais
# que precisem simular o ambiente.
_IN_RAILWAY = any(k.startswith("RAILWAY_") for k in os.environ)
_BYPASS = os.environ.get("MEDIDOR_ALLOW_DEFAULT_PASSWORD", "").lower() in ("1", "true", "yes")
if _IN_RAILWAY and _ADMIN_PASSWORD == "elos" and not _BYPASS:
    raise RuntimeError(
        "ERRO DE SEGURANÇA: MEDIDOR_ADMIN_PASSWORD está com o valor default "
        "('elos') em ambiente Railway. Configure uma senha forte na aba "
        "Variables do service antes de subir. Pra forçar boot mesmo assim "
        "(NÃO recomendado), defina MEDIDOR_ALLOW_DEFAULT_PASSWORD=1."
    )

_SESSION_SECRET = os.environ.get("MEDIDOR_SESSION_SECRET") or f"medidor-v1::{_ADMIN_PASSWORD}"

COOKIE_NAME = "medidor_session"
MAX_AGE_SEC = 60 * 60 * 24 * 7  # 7 dias
COOKIE_SECURE = os.environ.get("MEDIDOR_COOKIE_SECURE", "").lower() in ("1", "true", "yes")

_serializer = URLSafeTimedSerializer(_SESSION_SECRET, salt="medidor-admin-session")
_csrf_serializer = URLSafeTimedSerializer(_SESSION_SECRET, salt="medidor-csrf")
CSRF_FIELD = "_csrf"
CSRF_MAX_AGE_SEC = MAX_AGE_SEC


def verificar_credenciais(usuario: str, senha: str) -> bool:
    u_ok = secrets.compare_digest(usuario.encode("utf-8"), _ADMIN_USER.encode("utf-8"))
    p_ok = secrets.compare_digest(senha.encode("utf-8"), _ADMIN_PASSWORD.encode("utf-8"))
    return u_ok and p_ok


def criar_token_sessao(usuario: str) -> str:
    return _serializer.dumps(usuario)


def usuario_da_sessao(token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    try:
        return _serializer.loads(token, max_age=MAX_AGE_SEC)
    except (BadSignature, SignatureExpired):
        return None


def csrf_token_para(usuario: str) -> str:
    """Token CSRF derivado deterministicamente do usuário + secret. Permite
    renderizar no template e validar no submit sem precisar de storage."""
    return _csrf_serializer.dumps(usuario)


def csrf_valido(token: Optional[str], usuario: str) -> bool:
    if not token:
        return False
    try:
        loaded = _csrf_serializer.loads(token, max_age=CSRF_MAX_AGE_SEC)
        return secrets.compare_digest(loaded.encode("utf-8"), usuario.encode("utf-8"))
    except (BadSignature, SignatureExpired):
        return False


def autenticar_admin(request: Request) -> str:
    """Dependência: exige sessão válida. Redireciona pra /login se faltar/expirar."""
    usuario = usuario_da_sessao(request.cookies.get(COOKIE_NAME))
    if usuario is None:
        next_url = request.url.path
        if request.url.query:
            next_url = f"{next_url}?{request.url.query}"
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": f"/login?next={next_url}"},
        )
    return usuario


async def autenticar_admin_com_csrf(request: Request) -> str:
    """Como autenticar_admin, mas em POST/PUT/DELETE também valida CSRF token
    do form. Use em rotas POST do admin."""
    usuario = autenticar_admin(request)
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        form = await request.form()
        token = form.get(CSRF_FIELD)
        if not csrf_valido(token, usuario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sessão expirada ou requisição inválida. Recarregue a página e tente novamente.",
            )
    return usuario
