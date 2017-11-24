SHELL := /bin/bash

init:
	source /home/mats/.virtualenvs/cosytest/bin/activate; \
	mkdir -p ~/.config; \
	pip install .

unittest:
	python -m unittest

integration:
	source /home/mats/.virtualenvs/cosytest/bin/activate; \
	tests/integration.py

end-to-end: init integration



