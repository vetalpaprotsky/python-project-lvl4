run:
	poetry run ./manage.py runserver

shell:
	poetry run ./manage.py shell

lint:
	poetry run flake8 task_manager

.PHONY: run shell lint test
