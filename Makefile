RUN_PYTHON = docker-compose run --rm --entrypoint pipenv app run python

lint:
	$(RUN_PYTHON) -m pylint app

test: test_domain

test_domain:
	PYTHONDONTWRITEBYTECODE=1 $(RUN_PYTHON) -m pytest --pyargs app.domain.tests -x
