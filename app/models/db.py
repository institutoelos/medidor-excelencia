"""Schema do banco — fielmente seção 16.2 da especificação.

Tabelas:
- empresas
- rodadas
- respondentes_colab
- respondentes_socio
- respostas (itens Likert dos dois tipos de respondente)
- respostas_ancora
- respostas_nps
- respostas_retencao

Identificador anônimo: o token público do respondente, usado nos links únicos
de formulário, é separado do id interno. Confidencialidade é preservada.
"""
from __future__ import annotations

import os
import secrets
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    event,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

DB_PATH = os.environ.get(
    "MEDIDOR_DB_PATH",
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "medidor.db"),
)
DB_PATH = os.path.abspath(DB_PATH)

# Em produção (Railway), DATABASE_URL é injetada quando o serviço Postgres é
# adicionado. Localmente, sem essa var, caímos no SQLite por padrão.
_DATABASE_URL_RAW = os.environ.get("DATABASE_URL")
if _DATABASE_URL_RAW:
    # Railway/Heroku às vezes entregam postgres:// — SQLAlchemy 2 quer postgresql://
    if _DATABASE_URL_RAW.startswith("postgres://"):
        _DATABASE_URL_RAW = _DATABASE_URL_RAW.replace("postgres://", "postgresql+psycopg://", 1)
    elif _DATABASE_URL_RAW.startswith("postgresql://"):
        _DATABASE_URL_RAW = _DATABASE_URL_RAW.replace("postgresql://", "postgresql+psycopg://", 1)
    DATABASE_URL = _DATABASE_URL_RAW
    _IS_SQLITE = False
else:
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    _IS_SQLITE = True

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if _IS_SQLITE else {},
    echo=False,
    pool_pre_ping=not _IS_SQLITE,  # útil em conexões longas com Postgres
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def _now() -> datetime:
    return datetime.utcnow()


def _gerar_token(n: int = 24) -> str:
    return secrets.token_urlsafe(n)


# ─── Tabelas ────────────────────────────────────────────────────────────────

class Empresa(Base):
    __tablename__ = "empresas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    data_entrada: Mapped[datetime] = mapped_column(DateTime, default=_now)
    lista_de_areas: Mapped[str] = mapped_column(Text, default="")  # CSV simples
    tamanho_time_esperado: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    qtd_socios_esperados: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)

    rodadas: Mapped[list["Rodada"]] = relationship(back_populates="empresa", cascade="all, delete-orphan")

    def areas_lista(self) -> list[str]:
        return [a.strip() for a in (self.lista_de_areas or "").split(",") if a.strip()]


TIPOS_RODADA = ["entrada", "6m", "12m", "18m", "24m"]


class Rodada(Base):
    __tablename__ = "rodadas"
    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(8), nullable=False)  # entrada / 6m / 12m / 18m / 24m
    data_inicio: Mapped[datetime] = mapped_column(DateTime, default=_now)
    data_fim: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="aberta")  # aberta / fechada

    # Tokens públicos para os dois links
    token_colab: Mapped[str] = mapped_column(String(64), default=_gerar_token, unique=True, index=True)
    token_socio: Mapped[str] = mapped_column(String(64), default=_gerar_token, unique=True, index=True)

    empresa: Mapped["Empresa"] = relationship(back_populates="rodadas")
    respondentes_colab: Mapped[list["RespondenteColab"]] = relationship(back_populates="rodada", cascade="all, delete-orphan")
    respondentes_socio: Mapped[list["RespondenteSocio"]] = relationship(back_populates="rodada", cascade="all, delete-orphan")


class RespondenteColab(Base):
    __tablename__ = "respondentes_colab"
    id: Mapped[int] = mapped_column(primary_key=True)
    rodada_id: Mapped[int] = mapped_column(ForeignKey("rodadas.id"), nullable=False)
    # Token anônimo de sessão (não vincula identidade)
    sessao_token: Mapped[str] = mapped_column(String(64), default=_gerar_token, unique=True, index=True)
    tempo_de_casa: Mapped[Optional[str]] = mapped_column(String(32))
    tipo_de_cargo: Mapped[Optional[str]] = mapped_column(String(32))
    area: Mapped[Optional[str]] = mapped_column(String(120))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=_now)
    finalizado_em: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    rodada: Mapped["Rodada"] = relationship(back_populates="respondentes_colab")


class RespondenteSocio(Base):
    __tablename__ = "respondentes_socio"
    id: Mapped[int] = mapped_column(primary_key=True)
    rodada_id: Mapped[int] = mapped_column(ForeignKey("rodadas.id"), nullable=False)
    sessao_token: Mapped[str] = mapped_column(String(64), default=_gerar_token, unique=True, index=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=_now)
    finalizado_em: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    rodada: Mapped["Rodada"] = relationship(back_populates="respondentes_socio")


# Respostas Likert — usa polimorfismo por tipo_respondente (colab/socio)
class Resposta(Base):
    __tablename__ = "respostas"
    id: Mapped[int] = mapped_column(primary_key=True)
    respondente_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    tipo_respondente: Mapped[str] = mapped_column(String(8), nullable=False)  # 'colab' | 'socio'
    item_numero: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_likert: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..5
    __table_args__ = (
        UniqueConstraint("respondente_id", "tipo_respondente", "item_numero", name="uq_resposta_item"),
    )


class RespostaAncora(Base):
    __tablename__ = "respostas_ancora"
    id: Mapped[int] = mapped_column(primary_key=True)
    respondente_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    tipo_respondente: Mapped[str] = mapped_column(String(8), nullable=False)
    valor: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..5
    __table_args__ = (
        UniqueConstraint("respondente_id", "tipo_respondente", name="uq_ancora"),
    )


class RespostaNPS(Base):
    __tablename__ = "respostas_nps"
    id: Mapped[int] = mapped_column(primary_key=True)
    respondente_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    valor_0_10: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..10


class RespostaRetencao(Base):
    __tablename__ = "respostas_retencao"
    id: Mapped[int] = mapped_column(primary_key=True)
    respondente_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    opcao_escolhida: Mapped[str] = mapped_column(String(32), nullable=False)
    texto_aberto: Mapped[Optional[str]] = mapped_column(Text)


def init_db() -> None:
    if _IS_SQLITE:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)


# Cascade manual: ao deletar um respondente, limpa suas respostas (FK polimórfica)
def _limpar_respostas_colab(mapper, connection, target):
    from sqlalchemy import delete
    connection.execute(delete(Resposta).where(
        (Resposta.respondente_id == target.id) & (Resposta.tipo_respondente == "colab")
    ))
    connection.execute(delete(RespostaAncora).where(
        (RespostaAncora.respondente_id == target.id) & (RespostaAncora.tipo_respondente == "colab")
    ))
    connection.execute(delete(RespostaNPS).where(RespostaNPS.respondente_id == target.id))
    connection.execute(delete(RespostaRetencao).where(RespostaRetencao.respondente_id == target.id))


def _limpar_respostas_socio(mapper, connection, target):
    from sqlalchemy import delete
    connection.execute(delete(Resposta).where(
        (Resposta.respondente_id == target.id) & (Resposta.tipo_respondente == "socio")
    ))
    connection.execute(delete(RespostaAncora).where(
        (RespostaAncora.respondente_id == target.id) & (RespostaAncora.tipo_respondente == "socio")
    ))


event.listen(RespondenteColab, "before_delete", _limpar_respostas_colab)
event.listen(RespondenteSocio, "before_delete", _limpar_respostas_socio)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
