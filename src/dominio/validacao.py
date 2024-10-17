# src/dominio/validacao.py

"""
Módulo para validar caminhos de arquivos.

Este módulo oferece funcionalidade para verificar se os caminhos fornecidos
existem no sistema de arquivos e os classifica como válidos ou inválidos.
Inclui uma função principal que aceita uma lista de caminhos e retorna
um objeto JSON com o status de cada caminho.
"""

from pathlib import Path
from typing import Any, Dict, List


def validar_caminho(caminho: str) -> Dict[str, Any]:
    """
    Valida um caminho de arquivo e retorna o status em formato de dicionário.

    Esta função verifica a existência do caminho fornecido no sistema
    de arquivos. Retorna um dicionário onde a chave é "status" e o valor
    é o caminho absoluto, ou um aviso se o caminho não existir.

    Args:
        caminho (str): Caminho de arquivo a ser validado.

    Returns:
        Dict[str, Any]: Dicionário com o status do caminho.
    """
    path = Path(caminho).resolve()  # Converte para o caminho absoluto
    if not path.exists():
        return {"status": "NOT_OK", "caminho(s)": str(path)}
    return {"status": "ALL_OK", "caminho(s)": str(path)}


def validar_caminhos(caminhos: List[str]) -> Dict[str, List[str]]:
    """
    Valida uma lista de caminhos de arquivos e retorna um objeto JSON.

    Esta função verifica a existência de cada caminho fornecido no sistema
    de arquivos. Retorna um dicionário onde as chaves são "ALL_OK" e "NOT_OK",
    e os valores são listas de caminhos correspondentes.

    Args:
        caminhos (List[str]): Lista de caminhos de arquivos a serem validados.

    Returns:
        Dict[str, List[str]]: Dicionário com os status dos caminhos.
    """
    resultado: Dict[str, List[str]] = {"ALL_OK": [], "NOT_OK": []}

    for caminho in caminhos:
        resultado_individual = validar_caminho(caminho)
        # Adiciona o caminho à lista correspondente
        if resultado_individual["status"] == "ALL_OK":
            resultado["ALL_OK"].append(resultado_individual["caminho(s)"])
        else:
            resultado["NOT_OK"].append(resultado_individual["caminho(s)"])

    return resultado
