import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import tarefas

load_dotenv()

# Cria as tabelas que ainda nao existem, comparando com os modelos.
# Suficiente para um projeto didatico; em producao, o proximo passo seria
# o Alembic para migracoes versionadas.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TarefaFlow API",
    description="API de um quadro Kanban simples, feita para ensinar o ciclo "
    "completo de requisicao/resposta com FastAPI, SQLAlchemy e validacao Pydantic.",
    version="1.0.0",
)

origens_permitidas = [
    origem.strip()
    for origem in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origem.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tarefas.router)


@app.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
