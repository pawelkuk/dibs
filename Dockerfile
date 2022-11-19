FROM python:3.11-slim-buster

COPY requirements.txt /

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

WORKDIR /src/api
ENV DJANGO_SETTINGS_MODULE=api.settings
CMD pip install --target /my-site-packages -r /requirements.txt && \
    python /src/api/wait_for_postgres.py && \
    python /src/api/manage.py migrate && \
    python /src/api/manage.py migrate --database booking && \
    python /src/api/manage.py migrate --database paying && \
    python /src/api/manage.py migrate --database ticketing && \
    python /src/api/manage.py runserver 0.0.0.0:80
