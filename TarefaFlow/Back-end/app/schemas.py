"""
Schemas Pydantic: os formatos de dados que entram e saem pela API HTTP.

Por que 3 schemas diferentes para "a mesma" tarefa, em vez de um so?
  - TarefaCriar   -> so os campos que o CLIENTE deve enviar ao criar (POST).
                     O cliente nao escolhe o id nem as datas, entao esses
                     campos nem existem aqui.
  - TarefaAtualizar -> os mesmos campos de negocio, mas todos OPCIONAIS,
                     porque um PATCH pode alterar so um campo de cada vez
                     (ex.: so mover o status, sem reenviar o titulo).
  - TarefaResposta  -> o formato que a API DEVOLVE, incluindo campos que o
                     servidor controla (id, criado_em, atualizado_em).

Reutilizar um unico schema para as 3 situacoes forcaria campos como `id` a
serem opcionais na criacao (o que e uma mentira: o cliente nunca deveria
poder escolher o id) e tornaria dificil saber, so olhando o schema, o que
realmente e esperado em cada endpoint.

As respostas usam `camelCase` (ex.: `criadoEm`) para casar naturalmente com a
convencao do TypeScript/JavaScript no frontend, enquanto o Python por baixo
continua em `snake_case`, que e a convencao da linguagem.
"""

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
    """Corpo esperado em POST /api/tarefas."""

    titulo: str = Field(min_length=1, max_length=120)
    descricao: str | None = None


class TarefaAtualizar(_SchemaBase):
    """
    Corpo esperado em PATCH /api/tarefas/{id}.

    Todos os campos sao opcionais (default None): o cliente envia apenas o
    que deseja alterar. Campos ausentes no JSON permanecem `None` aqui e o
    router os ignora, mantendo o valor atual no banco.
    """

    titulo: str | None = Field(default=None, min_length=1, max_length=120)
    descricao: str | None = None
    status: StatusTarefa | None = None


class TarefaResposta(_SchemaBase):
    """Formato devolvido pela API em todas as rotas que retornam uma tarefa."""

    id: int
    titulo: str
    descricao: str | None
    status: StatusTarefa
    criado_em: datetime
    atualizado_em: datetime
