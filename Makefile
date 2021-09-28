include .env
SHELL=/bin/bash
ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin

start-app:
	django-admin startapp $(APP)

install:
	$(PIP) install -r requirements.txt

make-migrations:
	$(PYTHON) manage.py makemigrations $(APP)

migrate:
	$(PYTHON) manage.py migrate

serve:
	$(PYTHON) manage.py runserver

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
	isort .

clean-migrations:
	rm -rf **/migrations

create-superuser:
	$(PYTHON) manage.py createsuperuser

create-admin:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL) --noinput
