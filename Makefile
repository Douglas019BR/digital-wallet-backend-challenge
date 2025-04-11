.PHONY: build up down restart migrate seed test test-coverage

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

test-coverage:
	docker-compose exec web pytest --cov=app --cov-report=xml:/tmp/coverage/coverage.xml

format:
	ruff format .

format-check:
	ruff format --check --diff .

imports-fix:
	isort .

imports-fix-check:
	isort --check-only --diff .