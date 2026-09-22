"""
Dependencias reutilizaveis do FastAPI.

`get_db` implementa o padrao "uma sessao de banco por requisicao": a cada
requisicao HTTP, o FastAPI chama esta funcao geradora, que abre uma sessao
nova, a entrega para a rota via `yield`, e — depois que a rota termina, com
sucesso ou com erro — fecha a sessao no bloco `finally`. Nunca reaproveitamos
uma sessao entre requisicoes diferentes: isso evitaria vazamento de dados
entre requisicoes concorrentes e conexoes penduradas.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
