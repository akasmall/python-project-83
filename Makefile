.PHONY: install local-build load-env dev start

install:
	psql -a -d $$DATABASE_URL -f database.sql && poetry install

load-env:
	# @echo "Loading environment variables..."
	# @export $$(grep -v '^#' .env | xargs)
	@export $$(grep -v '^#' .env.dev | xargs)

local-build: load-env
	# DATABASE_URL=postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):5432/$(POSTGRES_DB)  && pip install poetry && poetry install
	# psql -a -d postgresql://aka_sm:myStrongPassword123!@localhost:5432/database -f database.sql && pip install poetry && poetry install
	# psql -a -d $$DATABASE_URL -f database.sql && \

	psql -a -d $${DATABASE_URL} -f database.sql && pip install poetry && poetry install

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
