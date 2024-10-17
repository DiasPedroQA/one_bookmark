# src/aplicacao/rotas.py
# pylint: disable=C0301, E0401

"""
Módulo de rotas para validação de caminhos de arquivos.

Este módulo define rotas da API para validar se os caminhos de arquivos
fornecidos são válidos ou não. Ele utiliza a função de validação definida
no módulo 'dominio.validacao'.
"""

from typing import Dict, List

from fastapi import APIRouter

from src.dominio.modelos import CaminhoSaidaDTO
from src.infraestrutura.logger import log_requisicao

router = APIRouter()


# Lista de exemplos de caminhos válidos e inválidos por sistema operacional
CAMINHOS_TESTE: Dict[str, Dict[str, List[str]]] = {
    "linux": {
        "paths_all_ok": ["/home/usuario/Downloads", "/etc/passwd"],
        "paths_not_ok": ["/home/usuario/Inexistente", "/invalid/path"],
    },
    "macos": {
        "paths_all_ok": ["/Users/usuario/Documents", "/System/Library"],
        "paths_not_ok": ["/Users/usuario/Inexistente", "/invalid/path"],
    },
    "windows": {
        "paths_all_ok": ["C:\\Usuarios\\usuario\\Documentos", "C:\\Windows\\System32"],
        "paths_not_ok": ["C:\\Usuarios\\usuario\\Inexistente", "Z:\\invalid\\path"],
    },
}


@router.get(path="/validar_caminhos/", response_model=CaminhoSaidaDTO)  # type: ignore
def validar_caminhos(caminhos: List[str]) -> CaminhoSaidaDTO:
    """
    Rota para validar uma lista de caminhos fornecidos.
    A função recebe uma lista de caminhos,
    verifica se eles são válidos ou inválidos, e retorna o resultado.

    Parâmetros:
        - caminhos (List[str]): Lista de caminhos a serem validados.

    Retorno:
        - CaminhoSaidaDTO: Contém as listas de caminhos válidos e inválidos.
    """
    paths_all_ok = []
    paths_not_ok = []

    for caminho in caminhos:
        if (
            caminho in CAMINHOS_TESTE["linux"]["paths_all_ok"]
            or caminho in CAMINHOS_TESTE["macos"]["paths_all_ok"]
            or caminho in CAMINHOS_TESTE["windows"]["paths_all_ok"]
        ):
            paths_all_ok.append(caminho)
            log_requisicao(caminho, sucesso=True)
        else:
            paths_not_ok.append(caminho)
            log_requisicao(caminho, sucesso=False)

    return CaminhoSaidaDTO(paths_all_ok=paths_all_ok, paths_not_ok=paths_not_ok)
