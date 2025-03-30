.PHONY: build up down restart migrate seed test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart: down up

migrate:
	docker-compose exec web alembic upgrade head

seed:
	docker-compose exec web python seeds/create_admin_user.py

test:
	docker-compose exec web pytest -svv