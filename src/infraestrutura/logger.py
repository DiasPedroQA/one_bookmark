"""
Módulo de Logger para registro de requisições.

Este módulo configura um logger para registrar informações sobre as requisições
de validação de caminhos. Os logs são gravados em um arquivo chamado
"log_requisicoes.log". O formato do log inclui a data e hora, o nível do log e
a mensagem correspondente.

Funções:
    - log_requisicao(caminho: str, sucesso: bool): Registra logs de requisições
        de validação de caminho, indicando se a validação foi bem-sucedida ou falhou.
"""

# src/infraestrutura/logger.py

import logging

# Configuração básica do logger
logging.basicConfig(
    filename="log_requisicoes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_requisicao(caminho: str, sucesso: bool) -> None:
    """
    Função para registrar logs de requisições de validação de caminho.

    Parâmetros:
        - caminho (str): O caminho que está sendo validado.
        - sucesso (bool): Indica se a validação foi bem-sucedida ou falhou.
    """
    if sucesso:
        logging.info("Requisição bem-sucedida: Caminho válido - %s", caminho)
    else:
        logging.warning("Requisição falhou: Caminho inválido - %s", caminho)
