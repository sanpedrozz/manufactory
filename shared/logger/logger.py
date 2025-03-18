import gzip
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler

LOG_DIR = "/app/logs"
LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5  # Храним 10 последних логов


# Функция для архивации логов
def compress_log_file(log_file_path):
    """Сжимает лог-файл в .gz и удаляет оригинал"""
    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as f_in:
            with gzip.open(f"{log_file_path}.gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(log_file_path)


def setup_logger(module_name, log_level_str):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_level = getattr(logging, log_level_str.upper(), logging.NOTSET)
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s - %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Консольный логгер
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Файловый логгер с ротацией
    log_file = os.path.join(LOG_DIR, f"{module_name}.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=LOG_FILE_SIZE, backupCount=BACKUP_COUNT, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
