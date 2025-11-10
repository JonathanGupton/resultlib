.PHONY: install test type docker-build docker-test

install:
	pip install -r dev-requirements.txt

test:
	pytest -q

type:
	mypy

docker-build:
	docker build -t resultlib:dev .

docker-test:
	docker run --rm resultlib:dev
