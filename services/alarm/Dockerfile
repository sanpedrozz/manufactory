# Этап сборки зависимостей
FROM python:3.13.0-slim-bookworm AS builder

# Настройки окружения
ENV TZ=Europe/Moscow \
    POETRY_VERSION=1.8.4 \
    PYTHONUNBUFFERED=on \
    PYTHONPATH=/app

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install colorlog

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY poetry.lock pyproject.toml /app/

# Установка зависимостей через Poetry
RUN poetry install --no-root --no-interaction --no-ansi -vvv

# Копирование кода проекта
COPY services/plc_data_hub/src /app/services/plc_data_hub/src
COPY shared /app/shared
COPY .env /app/.env

# Запуск сервиса (запускаем main.py с initialize_readers)
CMD ["python", "services/plc_data_hub/src/app.py"]
