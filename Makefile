SHELL=bash

bandit:
	poetry run bandit --recursive --exclude ./tests/ .

black:
	poetry run black .

build: test bandit safety
	poetry build

publish: build
	poetry publish

reorder-imports:
	poetry run reorder-python-imports --exit-zero-even-if-changed `find -name "*.py"`

test: black reorder-imports
	poetry run pytest -vv --cov

safety:
	poetry run safety check --full-report
