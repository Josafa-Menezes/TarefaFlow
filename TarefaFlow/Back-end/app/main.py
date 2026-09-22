"""
Ponto de entrada da aplicacao FastAPI.

Responsabilidades deste arquivo, e so estas: criar a instancia do FastAPI,
configurar o CORS, criar as tabelas do banco na inicializacao e incluir os
routers. A logica de negocio de cada rota vive em `routers/`, nao aqui.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import tarefas

load_dotenv()

# Cria as tabelas que ainda nao existem no banco, comparando com os modelos
# declarados em app/models.py. Isso e suficiente para um projeto didatico
# deste tamanho; em um projeto real, o proximo passo seria adotar o Alembic
# para gerenciar migracoes versionadas (alterar uma coluna existente, por
# exemplo, exige uma migracao de verdade — `create_all` so cria o que falta).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TarefaFlow API",
    description="API de um quadro Kanban simples, feita para ensinar o ciclo "
    "completo de requisicao/resposta com FastAPI, SQLAlchemy e validacao Pydantic.",
    version="1.0.0",
)

# As origens permitidas vem de uma variavel de ambiente para que, em outros
# ambientes (deploy, outra porta, etc.), baste alterar o .env — sem tocar
# neste codigo. Sem essa configuracao, o navegador bloqueia toda chamada
# `fetch` do frontend para o backend, silenciosamente, so avisando no
# console do navegador (nunca no terminal do backend).
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
    """Healthcheck simples, util para confirmar que o backend esta de pe."""
    return {"status": "ok"}


# Com o servidor rodando, a documentacao interativa (Swagger) fica disponivel
# automaticamente em http://localhost:8000/docs — o FastAPI a gera sozinho a
# partir das rotas e schemas acima, sem nenhuma linha de codigo extra. Vale a
# pena abrir essa rota no navegador: da para testar POST/PATCH/DELETE ali
# mesmo, sem precisar do frontend.
