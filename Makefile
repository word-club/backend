include .env
SHELL=/bin/bash
ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin
SETTINGS := backend.settings.dev

.PHONY: start-app
start-app:
	django-admin startapp $(APP)

.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: make-migrations
make-migrations:
	$(PYTHON) manage.py makemigrations $(APP)

.PHONY: migrate
migrate:
	$(PYTHON) manage.py migrate

.PHONY: serve
serve:
	$(PYTHON) manage.py runserver $(BASE_URL) --settings=$(SETTINGS)

.PHONY: dev
dev:
	$(PYTHON) manage.py runserver $(BASE_URL) --settings=backend.settings.dev

.PHONY: prod
prod:
	$(PYTHON) manage.py runserver $(BASE_URL) --settings=backend.settings.prod

.PHONY: shell
shell:
	$(PYTHON) manage.py shell

.PHONY: collect-static
collect-static:
	$(PYTHON) manage.py collectstatic

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
	$(PYTHON) manage.py createsuperuser

.PHONY: new-admin
new-admin:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL) --noinput

.PHONY: fresh-migrations
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

.PHONY: fresh
fresh: clean-db-migration fresh-migrations new-admin

.PHONY: test
test:
	$(PYTHON) manage.py test --settings=backend.settings.test $(TEST)
