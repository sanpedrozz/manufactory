import logging

logger = logging.getLogger("processors")


async def process_out_data(key: str, values: list):
    """Обработка данных для outDataNonVerify и outDataVerify."""
    for value in values:
        logger.info(f"Обрабатываю outData {key}: {value}")
        # Логика обработки данных


async def process_default(key: str, value):
    """Обработка данных по умолчанию для остальных ключей."""
    logger.info(f"Обрабатываю {key}: {value}")
    # Логика обработки данных


# Регистрируем обработчики
PROCESSORS = {
    "outDataNonVerify": process_out_data,
    "outDataVerify": process_out_data,
}
