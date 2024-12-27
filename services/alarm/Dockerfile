# Этап сборки зависимостей
FROM python:3.13.0-slim-bookworm

# Аргумент для пути
ARG BASE_PATH

# Настройки окружения
ENV TZ=Europe/Moscow \
    POETRY_VERSION=1.8.5 \
    PYTHONUNBUFFERED=on \
    PYTHONPATH=/app/

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends curl tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY $BASE_PATH/poetry.lock $BASE_PATH/pyproject.toml /app/

# Установка зависимостей через Poetry
RUN poetry install --no-root --no-interaction --no-ansi -vvv

# Копирование кода проекта
COPY $BASE_PATH/src /app/$BASE_PATH/src
COPY shared /app/shared
COPY .env /app/.env

# Запуск сервиса
CMD ["sh", "-c", "uvicorn services.alarm.src.app:app --host 0.0.0.0 --port ${UVICORN_PORT}"]
