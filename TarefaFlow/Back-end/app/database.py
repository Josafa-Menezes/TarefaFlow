"""
Configuracao central do banco de dados.

Por que este arquivo existe separado dos outros: o "engine" (a conexao com o
banco) e o "sessionmaker" (a fabrica de sessoes) sao objetos que devem existir
uma unica vez em toda a aplicacao. Se cada arquivo criasse o seu proprio
engine, teriamos multiplas conexoes concorrentes e possiveis inconsistencias.
Centralizar aqui e importar dele em todo o resto do app garante que exista
uma unica fonte de verdade.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Carrega variaveis do arquivo .env (se existir) para os.environ.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tarefaflow.db")

# `connect_args={"check_same_thread": False}` e necessario apenas para SQLite:
# por padrao o SQLite so permite que a thread que criou a conexao a utilize,
# mas o FastAPI pode atender uma requisicao em uma thread diferente. Isso e
# seguro aqui porque abrimos e fechamos uma sessao nova a cada requisicao
# (veja dependencies.py) em vez de compartilhar uma conexao global.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# `sessionmaker` e uma fabrica: cada chamada a `SessionLocal()` cria uma nova
# sessao independente. Isso e o que possibilita o padrao "uma sessao por
# requisicao" usado em dependencies.py.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Classe base declarativa da qual todos os modelos SQLAlchemy herdam."""

    pass
