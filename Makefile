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

seed:
	docker-compose exec web python seeds/create_seed.py

test:
	docker-compose exec web pytest -svv