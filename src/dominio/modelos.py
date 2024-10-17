"""
Módulo `modelos` do domínio.

Este módulo define os modelos de dados utilizados na aplicação para receber e
retornar informações através da API. Os modelos são baseados no Pydantic, que
valida automaticamente os dados de entrada e saída.

Modelos definidos:
    - `CaminhoEntradaDTO`: DTO para a estrutura de entrada que contém uma lista
        de caminhos de arquivos ou diretórios para validação.
    - `CaminhoSaidaDTO`: DTO para a estrutura de saída, contendo a lista de
        caminhos que foram validados, separando-os em válidos e inválidos.
"""

from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field


class CaminhoEntradaDTO(BaseModel):  # type: ignore
    """
    DTO para a estrutura de entrada que contém uma lista de caminhos.

    Atributos:
        caminhos (List[str]): Lista de caminhos a serem validados.
    """

    caminhos: List[str] = Field(..., description="Lista de caminhos a serem validados")


class CaminhoSaidaDTO(BaseModel):  # type: ignore
    """
    DTO para a estrutura de saída contendo caminhos válidos e inválidos.

    Atributos:
        ALL_OK (List[str]): Lista de caminhos válidos.
        NOT_OK (List[str]): Lista de caminhos inválidos.
    """

    ALL_OK: List[str] = Field([], description="Lista de caminhos válidos")
    NOT_OK: List[str] = Field([], description="Lista de caminhos inválidos")


def validar_caminho(caminho: str) -> Dict[str, str]:
    """
    Valida um caminho e retorna seu status.

    Parâmetros:
        caminho (str): O caminho a ser validado.

    Retorna:
        Dict[str, str]: Um dicionário com o status e o caminho.
    """
    path = Path(caminho).resolve()
    if path.exists():
        return {"status": "ALL_OK", "caminho": str(path)}

    return {"status": "NOT_OK", "caminho": str(path)}


def validar_caminhos(caminhos: List[str]) -> Dict[str, List[str]]:
    """
    Valida uma lista de caminhos e retorna os resultados.

    Parâmetros:
        caminhos (List[str]): Lista de caminhos a serem validados.

    Retorna:
        Dict[str, List[str]]: Um dicionário contendo listas de caminhos válidos
        e inválidos.
    """
    resultado_validacao: Dict[str, List[str]] = {"ALL_OK": [], "NOT_OK": []}
    for caminho in caminhos:
        resultado_individual = validar_caminho(caminho)
        if resultado_individual["status"] == "ALL_OK":
            resultado_validacao["ALL_OK"].append(resultado_individual["caminho"])
        else:
            resultado_validacao["NOT_OK"].append(resultado_individual["caminho"])

    return resultado_validacao
