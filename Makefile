SHELL=bash

black:
	poetry run black .

reorder-imports:
	poetry run reorder-python-imports --exit-zero-even-if-changed `find -name "*.py"`

test: black reorder-imports
	poetry run pytest -vv --cov
