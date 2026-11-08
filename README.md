# EcoSinergia-Projeto-de-Engenharia-de-Software-2026.2

Bem-vindo ao **Eco-Sinergia**, um projeto acadêmico de jogo digital não violento desenvolvido com Arquitetura de Microserviços, Agentes AI e Componentes de Software.

## 🏗 Arquitetura do Sistema
O projeto é dividido em 5 microserviços principais executados em containers Docker:
1. **API Gateway** (Porta 8000): Gerencia as requisições e serve a interface do jogo (Frontend).
2. **Player Service** (Porta 8001): Gerencia os dados e status do jogador.
3. **City Service** (Porta 8002): Gerencia o estado da cidade, construções e natureza.
4. **AI Agents Service** (Porta 8003): Simula as reações da população (impacto da poluição na felicidade).
5. **Recommendation Service** (Porta 8004): Sistema de dicas com base no estado atual da cidade.

## 🚀 Como rodar o projeto localmente

Pré-requisitos: Ter o **Docker** e o **Docker Compose** instalados na sua máquina.

1. Abra o terminal na pasta raiz deste projeto.
2. Execute o comando:
   ```bash
   docker-compose up --build
