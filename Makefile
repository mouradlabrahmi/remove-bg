lint:
	pre-commit run --all-files

rm:
	docker-compose down && docker-compose rm -f

rm_all:
	docker rm -f $(docker ps -aq)

pull:
	docker-compose pull

up:
	docker-compose up init && docker-compose up -d

ps:
	docker-compose ps

restart:
	make rm && make up

build:
	docker-compose build

test:
	docker-compose run --rm app pytest

integration_test:
	docker-compose run --rm app pytest -m integration

run_uwsgi:
	python manage.py collectstatic --no-input -v 0 && uwsgi --http :8000 --enable-threads --http-keepalive --processes 4 --wsgi-file config/wsgi.py --check-static /public_assets --static-map /static=/public_assets --static-map /media=/app/media --static-map /favicon.ico=/public_assets/favicon.ico --logto /dev/stdout --logto2 /dev/stderr --mimefile /etc/mime.types

mypy:
	docker-compose run --rm app mypy lnp_core

migrations:
	docker-compose run --rm app python manage.py makemigrations

migrate:
	docker-compose run --rm app python manage.py migrate

resetmigrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
db_backup:
	./scripts/db_backups.sh