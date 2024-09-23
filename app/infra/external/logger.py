import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


logger = setup_logger()


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)
