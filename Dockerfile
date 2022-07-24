FROM python:3.9-slim-buster

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

WORKDIR /src/api
ENV DJANGO_SETTINGS_MODULE=api.settings
CMD python /src/api/wait_for_postgres.py && \
    python /src/api/manage.py migrate && \
    python /src/api/manage.py runserver 0.0.0.0:80
