"""
Todas as rotas relacionadas a tarefas, agrupadas em um APIRouter.

Usar um APIRouter (em vez de registrar as rotas direto em `main.py`) e o
padrao do FastAPI para organizar uma API que cresce: cada dominio (aqui,
"tarefas") ganha seu proprio arquivo, e `main.py` so precisa incluir o
router com `app.include_router(...)`.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Tarefa
from app.schemas import TarefaAtualizar, TarefaCriar, TarefaResposta

router = APIRouter(prefix="/api/tarefas", tags=["tarefas"])


def _buscar_tarefa_ou_404(db: Session, tarefa_id: int) -> Tarefa:
    """
    Busca uma tarefa pelo id ou interrompe a requisicao com 404.

    Centralizar essa logica aqui evita repetir o mesmo `if tarefa is None:
    raise HTTPException(...)` em PATCH e em DELETE.
    """
    tarefa = db.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma tarefa encontrada com id={tarefa_id}.",
        )
    return tarefa


@router.get("", response_model=list[TarefaResposta])
def listar_tarefas(db: Session = Depends(get_db)) -> list[Tarefa]:
    """Lista todas as tarefas, mais recentes primeiro."""
    resultado = db.execute(select(Tarefa).order_by(Tarefa.criado_em.desc()))
    return list(resultado.scalars().all())


@router.post("", response_model=TarefaResposta, status_code=status.HTTP_201_CREATED)
def criar_tarefa(dados: TarefaCriar, db: Session = Depends(get_db)) -> Tarefa:
    """
    Cria uma tarefa nova.

    O Pydantic ja validou `dados` antes desta funcao rodar (titulo entre 1 e
    120 caracteres, etc.) — se a validacao tivesse falhado, o FastAPI teria
    devolvido 422 automaticamente e este codigo nunca seria executado.
    """
    # .strip() remove espacos em branco nas pontas, conforme a regra de negocio.
    tarefa = Tarefa(titulo=dados.titulo.strip(), descricao=dados.descricao)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)  # recarrega os campos gerados pelo banco (id, datas)
    return tarefa


@router.patch("/{tarefa_id}", response_model=TarefaResposta)
def atualizar_tarefa(
    tarefa_id: int, dados: TarefaAtualizar, db: Session = Depends(get_db)
) -> Tarefa:
    """
    Atualiza parcialmente uma tarefa (titulo, descricao e/ou status).

    `model_dump(exclude_unset=True)` retorna apenas os campos que o cliente
    de fato enviou no JSON — nao os que ficaram com o valor default `None`
    por omissao. Isso e o que torna o PATCH "parcial": enviar apenas
    `{"status": "concluido"}` nao apaga o titulo, por exemplo.
    """
    tarefa = _buscar_tarefa_ou_404(db, tarefa_id)

    campos_enviados = dados.model_dump(exclude_unset=True)
    for campo, valor in campos_enviados.items():
        if campo == "titulo" and isinstance(valor, str):
            valor = valor.strip()
        setattr(tarefa, campo, valor)

    db.commit()
    db.refresh(tarefa)  # atualizado_em e recalculado pelo onupdate do modelo
    return tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)) -> None:
    """Remove uma tarefa. Responde 204 (sem corpo) em caso de sucesso."""
    tarefa = _buscar_tarefa_ou_404(db, tarefa_id)
    db.delete(tarefa)
    db.commit()
