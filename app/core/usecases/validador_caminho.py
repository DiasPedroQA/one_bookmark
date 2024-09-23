import os
import logging

# Configuração do logger
logging.basicConfig(
    filename='app/logs/validacao.log',  # Caminho do arquivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def validar_caminho(caminho):
    """
    Valida se um caminho existe e se é um diretório ou um arquivo.

    :param caminho: O caminho a ser validado.
    :return: Uma tupla contendo (existe, tipo), onde tipo é 'diretorio', 'arquivo' ou 'invalido'.
    """
    if os.path.exists(caminho):
        if os.path.isdir(caminho):
            logging.info(f"'{caminho}' é um diretório.")
            return True, 'diretorio'
        elif os.path.isfile(caminho):
            logging.info(f"'{caminho}' é um arquivo.")
            return True, 'arquivo'
    else:
        logging.warning(f"'{caminho}' não existe.")
        return False, 'invalido'
