SHELL=bash

black:
	poetry run black .

reorder-imports:
	poetry run reorder-python-imports `find -name "*.py"`

test: black reorder-imports
	poetry run pytest -vv --cov
