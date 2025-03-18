import asyncio

from fastapi import FastAPI

from services.redis_to_db.src.utils import process_redis_to_db
from shared.logger import setup_logger

log = setup_logger(__name__, 'INFO')

app = FastAPI(title="Redis Worker API", version="1.0.0")

# Список задач для Redis воркеров
redis_worker_tasks = []


@app.on_event("startup")
async def on_startup():
    global redis_worker_tasks

    log.info("Приложение запускается, инициализация Redis воркеров...")

    redis_worker_tasks.append(asyncio.create_task(process_redis_to_db()))

    log.info("Приложение успешно запущено.")


@app.on_event("shutdown")
async def on_shutdown():
    global redis_worker_tasks

    for task in redis_worker_tasks:
        task.cancel()
    log.info("Все Redis воркеры остановлены.")
    log.info("Приложение остановлено.")
