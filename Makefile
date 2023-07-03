.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python3 -m ipm_school.manage migrate

.PHONY: migrations
migrations:
	poetry run python3 -m ipm_school.manage makemigrations

.PHONY: run-server
run-server:
	poetry run python3 -m ipm_school.manage runserver

.PHONY: superuser
superuser:
	poetry run python3 -m ipm_school.manage createsuperuser

.PHONY: update
update: install migrate;