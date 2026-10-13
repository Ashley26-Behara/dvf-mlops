.PHONY: install data clean test

install:
	pip install -r requirements.txt

data:
	python -m src.data.download --dept 75 92 93 94 --years 2021 2022 2023

clean:
	python -m src.data.clean

test:
	pytest -v
