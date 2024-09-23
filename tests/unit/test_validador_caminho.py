# tests/unit/test_validador_caminho.py

import pytest
from unittest.mock import patch
from app.core.usecases.validador_caminho import validar_caminho
from typing import Union, Any


# Testes para caminhos válidos
@pytest.mark.parametrize("caminho, esperado", [
    ("/caminho/para/arquivo.txt", 'arquivo'),  # Linux
    ("/caminho/para/diretorio/", 'diretorio'),  # Linux
    ("C:/caminho/para/arquivo.txt", 'arquivo'),  # Windows
    ("C:/caminho/para/diretorio/", 'diretorio'),  # Windows
])
def test_validar_caminho(caminho: str, esperado: str) -> None:
    """Teste a validação de caminhos válidos usando mocks."""

    with patch('os.path.exists') as mock_exists, \
        patch('os.path.isfile') as mock_isfile, \
         patch('os.path.isdir') as mock_isdir:

        # Configura o mock para os.path.exists retornar True
        mock_exists.return_value = True

        # Configura os mocks para isfile e isdir conforme o tipo esperado
        if esperado == 'arquivo':
            mock_isfile.return_value = True
            mock_isdir.return_value = False
        elif esperado == 'diretorio':
            mock_isfile.return_value = False
            mock_isdir.return_value = True
        else:
            mock_isfile.return_value = False
            mock_isdir.return_value = False

        resultado = validar_caminho(caminho)
        assert resultado == esperado


# Testes para caminhos inexistentes
def test_validar_caminho_inexistente() -> None:
    """Teste para validar um caminho inexistente."""

    caminhos = [
        "/caminho/nao/existe.txt",  # Linux
        "C:/caminho/nao/existe.txt"  # Windows
    ]

    for caminho in caminhos:
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False  # Simula que o caminho não existe
            resultado = validar_caminho(caminho)
            assert resultado == 'inexistente'


# Testes para caminhos inválidos
@pytest.mark.parametrize("caminho", [
    None,
    "",
    " ",
    0,
    0.5,
    [],
    ["caminho"],
    {},
    {"path": "caminho"},
    object(),
    lambda x: x,
    b"/home/usuario/projeto/",
    "/home/usuario/projeto/\x00",
    "C:/Users/usuario/projeto/\x00",
    "/caminho_invalido\\erro_misto/",
    "C:/Users/usuario/projeto/tests/unit/"
])
def test_validar_caminho_excecoes(caminho: Union[str, None, int, float, list, dict, object, bytes, Any]) -> None:
    """Teste a validação de caminhos para entradas inválidas."""

    with pytest.raises(ValueError):
        validar_caminho(caminho)
