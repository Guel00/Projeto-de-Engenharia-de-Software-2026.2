# EcoMissão - Jogo Digital Não Violento com Microserviços e Agente de IA

Projeto da disciplina **Engenharia de Software 2026.2**.

**Repositório:** https://github.com/Guel00/Projeto-de-Engenharia-de-Software-2026.2

## Ideia do jogo

EcoMissão é um jogo educativo e não violento no qual o jogador resolve pequenos desafios de sustentabilidade. Cada rodada apresenta uma situação cotidiana e três ações possíveis. O jogador ganha pontos ao escolher a alternativa mais sustentável. O microserviço **EcoGuia Agent** analisa o desempenho e devolve uma recomendação explicável de dificuldade/categoria e uma dica motivacional.

## Arquitetura

- **Frontend**: HTML, CSS e JavaScript.
- **API Gateway**: FastAPI, porta `8000`.
- **Player Service**: FastAPI + SQLite, porta `8001`.
- **Game Service**: FastAPI, porta `8002`.
- **EcoGuia Agent**: FastAPI, porta `8003`.
- **Docker Compose**: sobe e conecta todos os componentes.

```text
Navegador
   |
   v
Frontend :8080
   |
   v
API Gateway :8000
   |-------------|-------------------|
   v             v                   v
Player :8001   Game :8002        EcoGuia :8003
 SQLite        Desafios           Recomendação
```

## Como executar com Docker

Pré-requisito: Docker Desktop ou Docker Engine com Docker Compose.

```bash
git clone https://github.com/Guel00/Projeto-de-Engenharia-de-Software-2026.2.git
cd Projeto-de-Engenharia-de-Software-2026.2
docker compose up --build
```

Acesse:

- Jogo: `http://localhost:8080`
- Gateway / Swagger: `http://localhost:8000/docs`
- Player Service / Swagger: `http://localhost:8001/docs`
- Game Service / Swagger: `http://localhost:8002/docs`
- EcoGuia Agent / Swagger: `http://localhost:8003/docs`

Para encerrar:

```bash
docker compose down
```

## Fluxo principal

1. O jogador digita seu nome e inicia a partida.
2. O Gateway cria o jogador no Player Service.
3. O Gateway pede um desafio ao Game Service.
4. O jogador escolhe uma ação.
5. O Game Service avalia a escolha e calcula os pontos.
6. O Player Service atualiza a pontuação.
7. O EcoGuia Agent analisa o resultado e recomenda a próxima abordagem.
8. A interface exibe resultado, pontuação, dica do agente e estado dos microserviços.

## Endpoints principais do Gateway

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/health` | Saúde do Gateway |
| GET | `/api/services` | Lista todos os microserviços e estado |
| POST | `/api/start` | Cria/inicia jogador |
| GET | `/api/challenge` | Obtém desafio |
| POST | `/api/answer` | Avalia resposta, atualiza score e consulta agente |
| GET | `/api/player/{id}` | Consulta jogador |

## Técnicas de reuso

- Microserviços independentes com APIs REST.
- Componentes reutilizáveis no frontend (`renderServiceCard`, `renderChallenge`, `showMessage`).
- Contratos JSON padronizados.
- Funções de acesso a banco isoladas no Player Service.
- Lógica do agente isolada em `agent.py`, reutilizável pela API ou por testes.

## Metodologia

Scrum simplificado com 3 Sprints:

- Sprint 1: visão, backlog, protótipo e Game Service.
- Sprint 2: Player Service, API Gateway e integração.
- Sprint 3: EcoGuia Agent, interface, Docker Compose, testes e documentação.

## Testes rápidos sem Docker

```bash
python -m compileall gateway services
python -m unittest discover -s tests -v
```

## Estrutura

```text
.
├── docker-compose.yml
├── frontend/
├── gateway/
├── services/
│   ├── player/
│   ├── game/
│   └── agent/
├── tests/
└── docs/
```

## Licença acadêmica

Uso educacional para a disciplina de Engenharia de Software.
