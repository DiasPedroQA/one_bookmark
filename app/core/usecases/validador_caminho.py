import os
from typing import Tuple


def validar_caminho(caminho: str) -> Tuple[bool, str]:
    """
    Valida se um caminho é um diretório, um arquivo ou inválido.

    Args:
        caminho (str): O caminho a ser validado.

    Returns:
        Tuple[bool, str]: Um tupla onde o primeiro elemento é um booleano que indica se o caminho existe,
                          e o segundo é uma string que indica o tipo de caminho ('diretorio', 'arquivo', 'invalido').
    """
    if os.path.exists(caminho):
        if os.path.isdir(caminho):
            return True, 'diretorio'
        elif os.path.isfile(caminho):
            return True, 'arquivo'
    return False, 'invalido'
