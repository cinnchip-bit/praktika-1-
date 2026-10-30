.PHONY: run test

run:
	python src/main.py

test:
	python -m unittest discover -s tests -v
