import logging

import colorlog

# Создание объекта colorlog.ColoredFormatter
formatter = colorlog.ColoredFormatter(
    '%(asctime)s | %(log_color)s%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Создание объекта logging.StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Создание объекта logger
logging.basicConfig(level=logging.WARNING, handlers=[stream_handler])

# Создание объекта logger
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    try:
        raise ValueError("An example exception")
    except ValueError as e:
        logger.exception('Exception occurred')
