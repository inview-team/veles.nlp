all: install migrate run

install:
	pip install -r requirements.txt

migrate:
	python mig.py

run:
	python main.py

.PHONY: all install migrate run