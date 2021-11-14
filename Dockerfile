FROM python:3.9-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

FROM python-base
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./

RUN pipenv sync
COPY . .
