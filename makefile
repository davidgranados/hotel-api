build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart: down up

pip-install-venv:
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

lint-flake8:
	docker-compose run --rm app sh -c "flake8"

lint-black:
	docker-compose run --rm app sh -c "black --check /app"

lint-isort:
	docker-compose run --rm app sh -c "isort --check /app"

lint-black-fix:
	docker-compose run --rm app sh -c "black /app"

lint-isort-fix:
	docker-compose run --rm app sh -c "isort /app"

lint-check:	lint-isort lint-black lint-flake8

lint-fix:	lint-isort-fix lint-black-fix lint-flake8

test:
	docker-compose run --rm app sh -c "python manage.py test"

makemigrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations"

migrate:
	docker-compose run --rm app sh -c "python manage.py migrate"
