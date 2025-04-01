# Desafio Backend de Carteira Digital

[🇧🇷](#) | [🇺🇸](README.md)

Este projeto implementa uma API backend para um sistema de carteira digital usando FastAPI e PostgreSQL containerizado com Docker. O sistema permite gerenciamento de usuários, autenticação e operações de carteira.

## [Desafio Original](https://github.com/WL-Consultings/challenges/tree/main/backend)

## Justificativas
Esta implementação se concentra em arquitetura limpa, separação de responsabilidades e testabilidade. O projeto usa FastAPI pelos seus benefícios de desempenho e geração automática de documentação, SQLAlchemy para operações de banco de dados e Docker para ambientes consistentes de desenvolvimento e implantação.
Pelo desafio descartar completamente a parte de front-end, não faria o menor sentido usar uma camada de template, sendo assim o Django se tornaria uma bazuca para matar uma borboleta.
Apesar de experiencia previa e gostar muito do django-rest-framework e sua organização e testabilidade, acredito que sua curva de aprendizado é bem menor, tendo como vantagens a integração do ORM, migrations nativo, model user nativo, rotas de admin (esses recursos seriam subutilizados neste contexto de API pura) entre outros benéficios. Escolhi usar o FastApi por conta de sua [eficiência](https://fastapi.tiangolo.com/#performance) e simplicidade, como proposto rodar o sistema dentro de um container, escolher dependencias mais leves significa diretamente poupar recursos, somando esses dois fatores, podemos traduzir como um ganho de dinheiro (pensando em hospedagem)

Resumindo, optei pelo FastAPI devido a:

- Desempenho superior
- Eficiência operacional (menor consumo de recursos em containers)
- Validação e documentação automáticas (via type hints)
- Assincronicidade nativa (para escalabilidade vertical)
- Menor footprint técnico (sem componentes não-utilizados como admin/templates)

## 📋 Índice
- [Desafio Backend de Carteira Digital](#desafio-backend-de-carteira-digital)
  - [Desafio Original](#desafio-original)
  - [Justificativas](#justificativas)
  - [📋 Índice](#-índice)
  - [✨ Recursos](#-recursos)
  - [🛠️ Stack Tecnológico](#️-stack-tecnológico)
  - [🚀 Começando](#-começando)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
  - [Recursos Adicionais](#recursos-adicionais)
  - [Licença](#licença)

## ✨ Recursos
- Registro e autenticação de usuários
- Manipulação segura de senhas com bcrypt
- Autenticação baseada em JWT
- Gerenciamento de carteira (criar, depositar e transferir)
- Rastreamento de histórico de transações
- Migrações de banco de dados com Alembic
- Containerizado com Docker
- Suite de testes abrangente

## 🛠️ Stack Tecnológico
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) Framework web de alto desempenho para construção de APIs
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white) Kit de ferramentas SQL e ORM
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) Banco de dados relacional
- ![Alembic](https://img.shields.io/badge/Alembic-2D3B4D?style=for-the-badge) Ferramenta de migração de banco de dados
- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) Containerização
- ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) Validação de dados e gerenciamento de configurações
- ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white) Framework de testes
- ![Ruff](https://img.shields.io/badge/Ruff-000000?style=for-the-badge) & ![isort](https://img.shields.io/badge/isort-3776AB?style=for-the-badge) Formatação de código e ordenação de imports

## 🚀 Começando

### Pré-requisitos
- Docker e Docker Compose

### Instalação
1. Clone o repositório
```bash
git clone <repository-url>
cd digital-wallet-backend-challenge
```
2. Crie um arquivo .env a partir do modelo
```bash
cp .env.template .env
```
3. Construa e inicie os containers
```bash
make build
make up
```
4. Execute as migrações do banco de dados
```bash
make migrate
```
5. (Opcional) Popule o banco de dados com dados iniciais
```bash
make seed
```
6. A API estará disponível em http://localhost:8000

7. A documentação SWAGGER estará disponível em http://localhost:8000/docs

## Recursos Adicionais
Verifique comandos adicionais no Makefile [Makefile]

## Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).