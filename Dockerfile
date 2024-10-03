# Этап сборки зависимостей
FROM python:3.12.7-slim-bookworm AS builder

ENV TZ=Europe/Moscow
ENV POETRY_VERSION=1.7.0
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

# Установка зависимостей для сборки
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    curl \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR /scr
COPY pyproject.toml poetry.lock /scr/

# Установка зависимостей
RUN poetry install --no-interaction --no-ansi -vvv

COPY . /scr/

EXPOSE 7000

CMD ["poetry", "run", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
