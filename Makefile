include .env
SHELL=/bin/bash
ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin
SETTINGS := backend.settings.dev

start-app:
	django-admin startapp $(APP)

install:
	$(PIP) install -r requirements.txt

make-migrations:
	$(PYTHON) manage.py makemigrations $(APP)

migrate:
	$(PYTHON) manage.py migrate

serve:
	$(PYTHON) manage.py runserver $(BASE_URL) --settings=$(SETTINGS)

dev:
	$(PYTHON) manage.py runserver $(BASE_URL) --settings=backend.settings.dev

prod:
	$(PYTHON) manage.py runserver $(BASE_URL) --settings=backend.settings.prod

shell:
	$(PYTHON) manage.py shell

collect-static:
	$(PYTHON) manage.py collectstatic

isort:
	isort .

black:
	black .

lint:
	black .
	isort **/*.py

lint-with-flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


black-check:
	if ! black --check .; then black --diff .; exit 1; fi

isort-check:
	if ! isort -c **/*.py; then isort --diff **/*.py; exit 1; fi

clean-migrations:
	rm -rf **/migrations

clean-db:
	rm -rf media
	rm -rf db.sqlite3

clean-env:
	rm -rf venv

clean: clean-db clean-migrations clean-env

clean-db-migration: clean-db clean-migrations

create-superuser:
	$(PYTHON) manage.py createsuperuser

new-admin:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL) --noinput


fresh-migrations:
	make clean-migrations
	make make-migrations APP=account
	make migrate
	make make-migrations APP=hashtag
	make migrate
	make make-migrations APP=community
	make migrate
	make make-migrations APP=publication
	make migrate
	make make-migrations APP=comment
	make migrate
	make make-migrations APP=vote
	make migrate
	make make-migrations APP=share
	make migrate
	make make-migrations APP=bookmark
	make migrate
	make make-migrations APP=hide
	make migrate
	make make-migrations APP=report
	make migrate
	make make-migrations APP=avatar
	make migrate
	make make-migrations APP=cover
	make migrate
	make make-migrations APP=image
	make migrate
	make make-migrations APP=link
	make migrate
	make make-migrations APP=auth_code
	make migrate
	make make-migrations APP=block
	make migrate
	make make-migrations APP=notification
	make migrate
	make make-migrations APP=administration
	make migrate

fresh: clean-db-migration fresh-migrations new-admin

test:
	$(PYTHON) manage.py test --settings=backend.settings.test $(TEST)