from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from app.models import StatusTarefa


class _SchemaBase(BaseModel):
    """Base comum: gera aliases camelCase e aceita snake_case ou camelCase na entrada."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,  # permite construir a partir de um objeto SQLAlchemy
    )


class TarefaCriar(_SchemaBase):
    titulo: str = Field(min_length=1, max_length=120)
    descricao: str | None = None


class TarefaAtualizar(_SchemaBase):
    titulo: str | None = Field(default=None, min_length=1, max_length=120)
    descricao: str | None = None
    status: StatusTarefa | None = None


class TarefaResposta(_SchemaBase):
    id: int
    titulo: str
    descricao: str | None
    status: StatusTarefa
    criado_em: datetime
    atualizado_em: datetime