# TarefaFlow

Um quadro Kanban simples (A Fazer / Em Andamento / Concluido) construido para
ensinar, da forma mais direta possivel, como um frontend React conversa com
um backend Python real — com banco de dados, validacao e uma API REST
completa (CRUD).

Este e um projeto **monorepo** com duas pastas independentes:

```
tarefaflow/
  backend/    ← FastAPI + SQLAlchemy + SQLite
  frontend/   ← React 19 + TypeScript + Vite + TanStack Query
```

## Por que este app existe

Um tutorial anterior (TrilhaFit) ensinou React consumindo dados **somente
leitura** de um JSON estatico. O TarefaFlow fecha essa lacuna: aqui os dados
sao **escritos** de verdade, atraves de um backend real, com um banco que
persiste entre reinicializacoes do servidor.

O padrao central que o app existe para ensinar fica em
`frontend/src/hooks/useMutarTarefa.ts`: como usar `useMutation` do TanStack
Query (criar, atualizar, excluir) e invalidar a query `['tarefas']` para que
a lista na tela se atualize sozinha — sem gerenciar estado manualmente.

## Como rodar

### Backend

```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Com o servidor no ar:
- API em `http://localhost:8000`
- Documentacao interativa (Swagger) em `http://localhost:8000/docs` — da
  para testar todas as rotas ali mesmo, sem precisar do frontend.
- O arquivo `tarefaflow.db` (SQLite) e criado automaticamente na primeira
  execucao.

### Frontend

Em outro terminal:

```cmd
cd frontend
npm install
copy .env.example .env
npm run dev
```

O app abre em `http://localhost:5173`.

> Os dois servidores precisam estar rodando ao mesmo tempo. Se o backend
> cair, o frontend mostra um aviso de erro de conexao em vez de travar.

## Endpoints da API

| Metodo | Rota | Descricao |
|---|---|---|
| `GET` | `/api/tarefas` | Lista todas as tarefas |
| `POST` | `/api/tarefas` | Cria uma tarefa (`{ titulo, descricao? }`) |
| `PATCH` | `/api/tarefas/{id}` | Atualiza titulo, descricao e/ou status (parcial) |
| `DELETE` | `/api/tarefas/{id}` | Remove uma tarefa |
| `GET` | `/api/health` | Healthcheck |

## Estrutura

```
backend/
  app/
    main.py              ← instancia FastAPI, CORS, cria as tabelas
    database.py           ← engine, sessionmaker, Base
    models.py             ← modelo SQLAlchemy Tarefa
    schemas.py             ← TarefaCriar, TarefaAtualizar, TarefaResposta
    dependencies.py        ← get_db() — sessao de banco por requisicao
    routers/tarefas.py     ← as 5 rotas
  requirements.txt
  .env.example

frontend/
  src/
    types/tarefa.ts
    api/
      tarefas.service.ts   ← fetch para o backend, ErroDeConexao / ErroDaApi
      queryClient.ts
    hooks/
      useTarefas.ts         ← useQuery
      useMutarTarefa.ts      ← useCreateTarefa / useAtualizarTarefa (otimista) / useExcluirTarefa
    components/
      QuadroKanban.tsx
      ColunaKanban.tsx
      CartaoTarefa.tsx
      FormularioNovaTarefa.tsx
    App.tsx
    main.tsx
    index.css               ← sistema de design "quadro de cortica"
  .env.example
  package.json
```

## Exercicio de consolidacao

Depois de rodando, um bom exercicio e adicionar um campo `prioridade`
(alta/media/baixa) de ponta a ponta: modelo SQLAlchemy, schemas Pydantic,
tratamento no endpoint, tipo TypeScript e um indicador visual no
`CartaoTarefa`.

## Notas de escopo

Este app e deliberadamente pequeno — o objetivo e ensinar o ciclo completo
request/response com validacao e persistencia real, nao construir um produto
completo:

- `Base.metadata.create_all` cria as tabelas automaticamente; em um projeto
  real, o proximo passo seria adotar o **Alembic** para migracoes
  versionadas (alterar uma coluna existente exige uma migracao de verdade).
- Drag-and-drop entre colunas nao foi implementado — mover uma tarefa e feito
  pelo seletor no rodape do cartao. E um bom bonus para quem quiser ir alem.
