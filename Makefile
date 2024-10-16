install:
	psql -a -d $$DATABASE_URL -f database.sql && poetry install

local-build:
	DATABASE_URL="postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):5432/$(POSTGRES_DB)" && \
		psql -a -d $$DATABASE_URL -f database.sql && \
		pip install poetry && \
		poetry install

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
