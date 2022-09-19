black:
	poetry run black .

test: black
	poetry run pytest --cov
