.PHONY: build up down restart migrate seed test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart: down up

requirements:
	docker-compose exec web pip install -r requirements-dev.txt

migrate:
	docker-compose exec web alembic upgrade head

create-migration:
	@read -p "Enter migration name: " name; \
	docker-compose exec web alembic revision --autogenerate -m "$$name"

seed:
	docker-compose exec web python seeds/create_seed.py

test:
	docker-compose exec web pytest -svv

format:
	ruff format .

format-check:
	ruff format --check --diff .

imports-fix:
	isort .

imports-fix-check:
	isort --check-only --diff .