RUN_PYTHON = docker-compose run --rm --entrypoint pipenv app run python

test: test_domain test_flask test_django

lint:
# We have duplicate code between the Django and Flask app, and don't want to have a PyLint warning about that
	$(RUN_PYTHON) -m pylint app.domain
	$(RUN_PYTHON) -m pylint app.api.django
	$(RUN_PYTHON) -m pylint app.api.flask

test_domain:
	$(RUN_PYTHON) -m pytest --pyargs app.domain.tests

test_flask:
	$(RUN_PYTHON) -m pytest --pyargs app.api.flask

test_django:
	$(RUN_PYTHON) src/app/api/django/manage.py test

pipenv_shell:
	docker-compose run --rm --entrypoint pipenv \
		app shell --fancy

start_django:
	docker-compose run --rm --entrypoint pipenv \
		-p 5000:5000 \
		app run python src/app/api/django/manage.py runserver 0:5000

start_flask:
	docker-compose run --rm --entrypoint pipenv \
		-e FLASK_APP=app.api.flask \
		-e FLASK_DEBUG=1 \
		-p 5000:5000 \
		app run python -m flask run --host=0.0.0.0
