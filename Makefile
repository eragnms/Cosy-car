init:
	pip install -r requirements.txt
	pip install .

test:
	python -m unittest

integration:
	tests/cosycar_integration.py
