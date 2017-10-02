init:
	pip install -r requirements.txt
	pip install .

unittest:
	python -m unittest

integration:
	tests/cosycar_integration.py

end-to-end:
	pip install -r requirements.txt
	pip install .
	tests/cosycar_integration.py
