FROM python:3
WORKDIR /usr/src/app
COPY . .
#RUN mkdir tests
#COPY tests/integration.py ./tests
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .
ENTRYPOINT ["./docker-entrypoint"]


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
