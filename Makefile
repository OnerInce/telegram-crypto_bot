format:
	python -m black -S --line-length 120 .

isort:
	isort .

type:
	mypy --ignore-missing-imports --exclude /venv/ .

lint:
	flake8 --max-line-length 120 ./src

ci: isort format type lint