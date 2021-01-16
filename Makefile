run:
	poetry run ./manage.py runserver

shell:
	poetry run ./manage.py shell

gunicorn:
	poetry run gunicorn task_manager.wsgi

update-requirements:
	poetry run pip freeze > requirements.txt

install:
	poetry install --no-root

test:
	poetry run pytest task_manager --cov=task_manager --log-cli-level=20

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck test lint

.PHONY: run shell install test lint selfcheck check
