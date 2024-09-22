# tests/unit/test_validador_caminho.py

import pytest
from app.core.usecases.validador_caminho import validar_caminho


# Teste para validar caminhos
@pytest.mark.parametrize("caminho, esperado", [
    ("tests/unit/test_validador_caminho.py", 'arquivo'),
    ("tests/unit/", 'diretório'),
    ("caminho/nao/existe.txt", 'inexistente')
])
def test_validar_caminho(caminho, esperado):
    """Teste a validação de caminhos."""
    assert validar_caminho(caminho) == esperado


# Teste para exceções
@pytest.mark.parametrize("caminho", [
    None,
    "",
    "invalid/path/to/file"
])
def test_validar_caminho_excecoes(caminho):
    """Teste a validação de caminhos para entradas inválidas."""
    with pytest.raises(ValueError):  # Ajuste para a exceção correta
        validar_caminho(caminho)
