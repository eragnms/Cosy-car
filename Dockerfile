FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir .
CMD ["python", "/tests/cosycar_integaration.py"]


#init:
#        pip install -r requirements.txt
#        pip install .
#
#unittest:
#        python -m unittest
#
#integration:
#        tests/cosycar_integration.py
#
#end-to-end: init unittest integration
