# app/core/usecases/validador_caminho.py

from pathlib import Path


def validar_caminho(caminho):
    """
    Valida se o caminho é válido e se corresponde a um arquivo ou diretório.
    Retorna uma string indicando o tipo do caminho ('arquivo' ou 'diretório')
    ou 'inexistente' se o caminho não for válido.
    """
    if caminho is None or not isinstance(caminho, str):
        raise ValueError("O caminho deve ser uma string não vazia.")

    path = Path(caminho)

    if path.exists():
        if path.is_file():
            return 'arquivo'
        elif path.is_dir():
            return 'diretório'
    return 'inexistente'
