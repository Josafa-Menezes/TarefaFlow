import enum
from datetime import datetime, timezone
from sqlalchemy import Enum as SqlEnum, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class StatusTarefa(str, enum.Enum):
    A_FAZER = "a_fazer"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"


def _agora() -> datetime:
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
