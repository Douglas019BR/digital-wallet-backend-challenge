# Digital Wallet Backend Challenge ![Coverage](https://github.com/Douglas019BR/digital-wallet-backend-challenge/blob/coverage-badge/coverage.svg)

This project implements a backend API for a digital wallet system using FastAPI and PostgreSQL containerized with Docker. The system allows for user management, authentication, and wallet operations.

## [Original Challenge](https://github.com/WL-Consultings/challenges/tree/main/backend)

## Justifications 
<!-- alterar -->
This implementation focuses on clean architecture, separation of concerns, and testability. The project uses FastAPI for its performance benefits and automatic documentation generation, SQLAlchemy for database operations, and Docker for consistent development and deployment environments.

## 📋 Table of Contents

- [Digital Wallet Backend Challenge ](#digital-wallet-backend-challenge-)
  - [Original Challenge](#original-challenge)
  - [Justifications](#justifications)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🛠️ Tech Stack](#️-tech-stack)
  - [🚀 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Additional Features](#additional-features)
  - [License](#license)

## ✨ Features
- User registration and authentication
- Secure password handling with bcrypt
- JWT-based authentication
- Wallet management (create, deposit, withdraw, transfer)
- Transaction history tracking
- Database migrations with Alembic
- Containerized with Docker
- Comprehensive test suite

## 🛠️ Tech Stack

- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) High-performance web framework for building APIs
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white) SQL toolkit and ORM
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) Relational database
- ![Alembic](https://img.shields.io/badge/Alembic-2D3B4D?style=for-the-badge) Database migration tool
- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) Containerization
- ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) Data validation and settings management
- ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white) Testing framework
- ![Ruff](https://img.shields.io/badge/Ruff-000000?style=for-the-badge) & ![isort](https://img.shields.io/badge/isort-3776AB?style=for-the-badge) Code formatting and import sorting

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Make (optional, for using Makefile commands)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd digital-wallet-backend-challenge
```

2. Create a .env file from the template
```bash
cp .env.template .env
```

3. Build and start the containers
```bash
make build
make up
```

4. Run database migrations
```bash
make migrate
```

5. (Optional) Seed the database with initial data
```bash
make seed
```

6. The API will be available at http://localhost:8000

## Additional Features
Check for additional commands in the Makefile [Makefile]

## License

This project is licensed under the [MIT License](LICENSE).

