FROM python:3
WORKDIR /usr/src/app
COPY . .
COPY tests/integration.py ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .
CMD ["./integration.py"]


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
