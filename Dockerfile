FROM python:3.9-slim-buster

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /src
ENV FLASK_APP=booking/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask --help && flask run --host=0.0.0.0 --port=80
