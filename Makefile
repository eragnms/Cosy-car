SHELL := /bin/bash

init:
	source /home/mats/.virtualenvs/cosy/bin/activate; \
	pip install .

unittest:
	python -m unittest

integration:
	source /home/mats/.virtualenvs/cosy/bin/activate; \
	tests/cosycar_integration.py

end-to-end: init integration



