run:
	poetry run ./manage.py runserver

shell:
	poetry run ./manage.py shell

gunicorn:
	poetry run gunicorn task_manager.wsgi

update-requirements:
	poetry run pip freeze > requirements.txt

create-ru-translations:
	poetry run ./manage.py makemessages -l ru

compile-ru-translations:
	poetry run ./manage.py compilemessages -l ru

create-uk-translations:
	poetry run ./manage.py makemessages -l uk

compile-uk-translations:
	poetry run ./manage.py compilemessages -l uk

install:
	poetry install --no-root

test:
	poetry run coverage run --source='task_manager' manage.py test

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck test lint

.PHONY: run shell gunicorn update-requirements install test lint selfcheck check
