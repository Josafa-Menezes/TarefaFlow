import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tarefaflow.db")

# connect_args é necessário só para SQLite: por padrão o SQLite só permite
# que a thread que criou a conexão a utilize, mas o FastAPI pode atender
# uma requisição em uma thread diferente.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Classe base declarativa da qual todos os modelos SQLAlchemy herdam."""
    pass
