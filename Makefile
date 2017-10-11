RUN_PYTHON = docker-compose run --rm --entrypoint pipenv app run python

test: test_domain test_app

test_domain:
	PYTHONDONTWRITEBYTECODE=1 $(RUN_PYTHON) -m pytest --pyargs app.domain.tests --pylint app

test_app:
	PYTHONDONTWRITEBYTECODE=1 $(RUN_PYTHON) -m pytest --pyargs app.api --pylint app

start_dev:
	docker-compose run --rm --entrypoint pipenv \
		-e PYTHONPATH=/app/src \
		-e FLASK_APP=app.api \
		-e FLASK_DEBUG=1 \
		-e WORKON_HOME=/app/pipenv \
		-p 5000:5000	 \
		app run python -m flask run --host=0.0.0.0
