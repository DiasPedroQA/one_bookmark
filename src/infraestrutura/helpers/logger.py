# src/infraestrutura/helpers/logger.py

"""
Este módulo fornece uma configuração de logger para o projeto.

O logger é utilizado para registrar mensagens em diferentes níveis de severidade,
como DEBUG, INFO, WARNING, ERROR e CRITICAL. A configuração permite que as
mensagens sejam registradas em um arquivo e exibidas no console.

Exemplo de uso:
    from src.infraestrutura.helpers.logger import logaritmo

    logger = logaritmo(__name__)
    logger.info("Esta é uma mensagem informativa.")
"""

import logging
from pathlib import Path


def configurar_logger(nome: str) -> logging.Logger:
    """
    Configura e retorna um logger para o módulo especificado.

    Args:
        nome (str): O nome do módulo que está usando o logger. Geralmente,
                    é o __name__ do módulo.

    Returns:
        logging.Logger: Um objeto Logger configurado para o módulo.
    """
    # Criar um diretório para armazenar logs, se não existir
    Path("logs").mkdir(parents=True, exist_ok=True)

    # Configuração básica do logger
    logging.basicConfig(
        level=logging.DEBUG,  # Nível mínimo de severidade das mensagens
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log"),  # Log em arquivo
            logging.StreamHandler(),  # Log no console
        ],
    )

    # Retorna um logger configurado
    logger = logging.getLogger(nome)
    return logger


def logaritmo(nome: str) -> logging.Logger:
    """
    Retorna um logger configurado para o módulo especificado.

    Args:
        nome (str): O nome do módulo que está usando o logger.

    Returns:
        logging.Logger: Um objeto Logger configurado para o módulo.
    """
    return configurar_logger(nome)
