include .env
SHELL=/bin/bash
ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin
SETTINGS := backend.settings.dev

.PHONY: start-app
start-app:
	django-admin startapp $(APP)

.PHONY: p-install
p-install:
	$(PIP) install $(PACKAGE)

.PHONY: pip-freeze
pip-freeze:
	$(PIP) freeze > requirements.txt

.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: make-migrations
make-migrations:
	$(PYTHON) manage.py makemigrations $(APP) --settings=$(SETTINGS)

.PHONY: migrate
migrate:
	$(PYTHON) manage.py migrate --settings=$(SETTINGS)

.PHONY: serve
serve:
	$(PYTHON) manage.py runserver $(HOST):$(PORT) --settings=$(SETTINGS)

.PHONY: dev
dev:
	$(PYTHON) manage.py runserver $(HOST):$(PORT) --settings=backend.settings.dev

.PHONY: prod
prod:
	$(PYTHON) manage.py runserver $(HOST):$(PORT) --settings=backend.settings.prod

.PHONY: shell
shell:
	$(PYTHON) manage.py shell --settings=$(SETTINGS)

.PHONY: collect-static
collect-static:
	$(PYTHON) manage.py collectstatic --settings=$(SETTINGS)

.PHONY: black
black:
	black .

.PHONY: lint
lint:
	black .

.PHONY: lint-with-flake8
lint-with-flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: black-check
black-check:
	if ! black --check .; then black --diff .; exit 1; fi

.PHONY: clean-migrations
clean-migrations:
	rm -rf **/migrations

.PHONY: clean-db
clean-db:
	rm -rf media
	rm -rf db.sqlite3

.PHONY: clean-env
clean-env:
	rm -rf venv


.PHONY: clean
clean: clean-db clean-migrations clean-env

.PHONY: clean-db-migration
clean-db-migration: clean-db clean-migrations

.PHONY: create-superuser
create-superuser:
	$(PYTHON) manage.py createsuperuser --settings=$(SETTINGS)

.PHONY: new-admin
new-admin:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL) --noinput --settings=$(SETTINGS)

.PHONY: fresh-migrations
fresh-migrations:
	make clean-migrations
	make make-migrations APP=account
	make make-migrations APP=hashtag
	make make-migrations APP=community
	make make-migrations APP=publication
	make make-migrations APP=comment
	make make-migrations APP=vote
	make make-migrations APP=bookmark
	make make-migrations APP=share
	make make-migrations APP=hide
	make make-migrations APP=block
	make make-migrations APP=avatar
	make make-migrations APP=cover
	make make-migrations APP=image
	make make-migrations APP=link
	make make-migrations APP=auth_code
	make make-migrations APP=report
	make make-migrations APP=notification
	make make-migrations APP=administration
	make migrate

.PHONY: fresh
fresh: clean-db-migration fresh-migrations new-admin

.PHONY: test
test:
	$(PYTHON) manage.py test --settings=backend.settings.test
