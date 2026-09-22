from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Tarefa
from app.schemas import TarefaAtualizar, TarefaCriar, TarefaResposta

router = APIRouter(prefix="/api/tarefas", tags=["tarefas"])


def _buscar_tarefa_ou_404(db: Session, tarefa_id: int) -> Tarefa:
    tarefa = db.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma tarefa encontrada com id={tarefa_id}.",
        )
    return tarefa


@router.get("", response_model=list[TarefaResposta])
def listar_tarefas(db: Session = Depends(get_db)) -> list[Tarefa]:
    resultado = db.execute(select(Tarefa).order_by(Tarefa.criado_em.desc()))
    return list(resultado.scalars().all())


@router.post("", response_model=TarefaResposta, status_code=status.HTTP_201_CREATED)
def criar_tarefa(dados: TarefaCriar, db: Session = Depends(get_db)) -> Tarefa:
    tarefa = Tarefa(titulo=dados.titulo.strip(), descricao=dados.descricao)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)  # recarrega os campos gerados pelo banco (id, datas)
    return tarefa


@router.patch("/{tarefa_id}", response_model=TarefaResposta)
def atualizar_tarefa(
    tarefa_id: int, dados: TarefaAtualizar, db: Session = Depends(get_db)
) -> Tarefa:
    tarefa = _buscar_tarefa_ou_404(db, tarefa_id)

    # exclude_unset=True: so os campos que o cliente de fato enviou no JSON.
    # E isso que torna o PATCH "parcial" — {"status": "concluido"} sozinho
    # nao apaga o titulo.
    campos_enviados = dados.model_dump(exclude_unset=True)
    for campo, valor in campos_enviados.items():
        if campo == "titulo" and isinstance(valor, str):
            valor = valor.strip()
        setattr(tarefa, campo, valor)

    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)) -> None:
    tarefa = _buscar_tarefa_ou_404(db, tarefa_id)
    db.delete(tarefa)
    db.commit()