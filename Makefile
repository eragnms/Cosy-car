SHELL := /bin/bash

init:
	source /home/mats/.virtualenvs/cosytest/bin/activate; \
	pip install -r requirements.txt; \
	pip install .

unittest:
	python -m unittest

integration:
	source /home/mats/.virtualenvs/cosytest/bin/activate; \
	tests/integration.py

end-to-end: init integration



