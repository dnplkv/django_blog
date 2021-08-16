include .env
export $(shell sed 's/=.*//' .env)
MANAGE = python core/manage.py
PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000


run:
	$(MANAGE) runserver 0.0.0.0:$(WSGI_PORT)

make-migrate:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

freeze:
	pip freeze > requirements.txt

flake:
	flake8 ./core