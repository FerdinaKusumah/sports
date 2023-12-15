run:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

export:
	poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt && \
		pip install -r requirements.txt && \
		rm -rf requirements.txt

migrate:
	poetry run python manage.py migrate

install:
	poetry install

update:
	poetry update

dump:
	poetry run python manage.py dumpdata --indent 2 > fixtures/db.json

restore:
	poetry run python manage.py loaddata fixtures/db.json
