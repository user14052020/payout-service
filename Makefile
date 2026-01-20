.PHONY: install migrate run worker test seed typecheck docker-up docker-down

install:
	python -m pip install -r requirements.txt

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

worker:
	celery -A payout_service worker -l info

test:
	python manage.py test

typecheck:
	mypy payout_service payouts

seed:
	python manage.py seed_payouts

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v
