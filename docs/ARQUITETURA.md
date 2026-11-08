# Arquitetura do EcoMissão

Frontend (:8080) -> API Gateway (:8000) -> Player Service (:8001, SQLite), Game Service (:8002) e EcoGuia Agent (:8003).

O EcoGuia é um agente simples e explicável: observa score, streak, último resultado e categoria, aplica regras e produz uma recomendação.
