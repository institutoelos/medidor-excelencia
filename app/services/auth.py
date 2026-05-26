"""Autenticação simples para o painel admin via HTTP Basic.

Senha vem da variável MEDIDOR_ADMIN_PASSWORD. Em modo dev (sem var), usa 'elos'.
Usuário padrão 'admin' (configurável via MEDIDOR_ADMIN_USER).
"""
from __future__ import annotations

import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

_ADMIN_USER = os.environ.get("MEDIDOR_ADMIN_USER", "admin")
_ADMIN_PASSWORD = os.environ.get("MEDIDOR_ADMIN_PASSWORD", "elos")

_security = HTTPBasic(realm="Medidor de Excelencia ELOS - Painel")


def autenticar_admin(creds: HTTPBasicCredentials = Depends(_security)) -> str:
    user_ok = secrets.compare_digest(creds.username.encode("utf-8"), _ADMIN_USER.encode("utf-8"))
    pwd_ok = secrets.compare_digest(creds.password.encode("utf-8"), _ADMIN_PASSWORD.encode("utf-8"))
    if not (user_ok and pwd_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": 'Basic realm="Medidor - Painel"'},
        )
    return creds.username
