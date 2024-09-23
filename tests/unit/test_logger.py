import logging
from app.infra.external.logger import setup_logger, log_info, log_error


def test_logger_setup():
    logger = setup_logger()
    assert logger.level == logging.INFO


def test_log_info(caplog):
    log_info("Teste de log de informação")
    assert "Teste de log de informação" in caplog.text


def test_log_error(caplog):
    log_error("Teste de log de erro")
    assert "Teste de log de erro" in caplog.text
