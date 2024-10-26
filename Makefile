PORT ?= 8888

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app --debug run --port $(PORT)

lint:
	poetry run flake8 page_analyzer

build:
	./build.sh

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
