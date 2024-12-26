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
logger = logging.getLogger(__name__)

logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    logger.exception('Exception message')
    raise ValueError("An example exception")
