# app/core/usecases/validador_caminho.py

from pathlib import Path


def validar_caminho(caminho):
    """
    Valida se o caminho é válido e se corresponde a um arquivo ou diretorio.
    Retorna uma string indicando o tipo do caminho ('arquivo' ou 'diretorio')
    ou 'inexistente' se o caminho não for válido.
    """
    if caminho is None or not isinstance(caminho, str) or caminho.strip() == "":
        raise ValueError("O caminho deve ser uma string não vazia.")

    path = Path(caminho)
    if not path.exists():
        return 'inexistente'
    elif path.is_dir():
        return 'diretorio'
    elif path.is_file():  # Verifique se é um arquivo
        return 'arquivo'
    else:
        return 'inexistente'  # Para casos onde não é nem arquivo nem diretorio
