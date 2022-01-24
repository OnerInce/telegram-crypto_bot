format:
	python -m black -S --line-length 120 .

isort:
	isort .

type:
	mypy -p src --ignore-missing-imports

lint:
	flake8 --max-line-length 120 ./src

ci: isort format type lint