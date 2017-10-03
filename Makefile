init:
	pip install -r requirements.txt
	pip install .

unittest:
	python -m unittest

integration:
	tests/cosycar_integration.py

end-to-end: init unittest integration



