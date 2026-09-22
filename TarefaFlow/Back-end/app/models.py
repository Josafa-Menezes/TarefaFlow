"""
Modelo SQLAlchemy: a representacao da tabela `tarefas` no banco de dados.

Importante nao confundir isto com os schemas Pydantic (schemas.py). O modelo
SQLAlchemy descreve a TABELA e como o Python conversa com o banco; os schemas
Pydantic descrevem os formatos de dados que entram e saem pela API. Sao duas
responsabilidades diferentes mesmo que os campos se pareçam.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class StatusTarefa(str, enum.Enum):
    """
    Os 3 unicos valores validos para o status de uma tarefa.

    Usar um Enum (em vez de aceitar qualquer string) faz o banco e a API
    rejeitarem automaticamente valores invalidos como "em_progresso" ou
    "feito" — apenas estes 3 nomes exatos sao aceitos.
    """

    A_FAZER = "a_fazer"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"


def _agora() -> datetime:
    """Horario atual em UTC, usado como default para as colunas de data."""
    return datetime.now(timezone.utc)


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[StatusTarefa] = mapped_column(
        SqlEnum(StatusTarefa, native_enum=False, length=20),
        default=StatusTarefa.A_FAZER,
        nullable=False,
    )
    criado_em: Mapped[datetime] = mapped_column(default=_agora, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(
        default=_agora,
        onupdate=_agora,  # SQLAlchemy atualiza este campo sozinho a cada UPDATE
        nullable=False,
    )
