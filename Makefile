.PHONY: build up down logs shell migrate migrate-up

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec api /bin/sh

migrate-create:
	@read -p "Message: " m && docker compose run --rm api alembic revision --autogenerate -m "$$m"

migrate-up:
	docker compose run --rm api alembic upgrade head
