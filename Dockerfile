FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN mkdir -p ~/.config
RUN pip install --no-cache-dir .
ENTRYPOINT ["./docker-entrypoint"]
