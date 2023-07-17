FROM python:3.8.6-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt update \
    && pip install --upgrade pip \
    && pip install poetry==1.5.1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-root

COPY . .

EXPOSE 8000

WORKDIR ./src

CMD uvicorn main:app --proxy-headers --forwarded-allow-ips=* --workers 8 --host 0.0.0.0 --port 8000 --no-access-log

