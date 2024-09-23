# tests/unit/test_validador_caminho.py

import pytest
from app.core.usecases.validador_caminho import validar_caminho


# Teste para validar caminhos em diferentes sistemas operacionais
@pytest.mark.parametrize("caminho, esperado", [
    # Caminhos válidos para Linux/Ubuntu/Mac
    ("/home/usuario/projeto/tests/unit/test_validador_caminho.py", 'arquivo'),
    ("/home/usuario/projeto/tests/unit/", 'diretorio'),

    # Caminhos válidos para Windows
    ("C:\\Users\\usuario\\projeto\\tests\\unit\\test_validador_caminho.py", 'arquivo'),
    ("C:\\Users\\usuario\\projeto\\tests\\unit\\", 'diretorio'),

    # Caminhos inexistentes
    ("/caminho/nao/existe.txt", 'inexistente'),
    ("C:\\caminho\\nao\\existe.txt", 'inexistente')
])
def test_validar_caminho(caminho, esperado):
    """Teste a validação de caminhos em diferentes sistemas operacionais."""
    assert validar_caminho(caminho) == esperado


# Teste para validar exceções com entradas inválidas
@pytest.mark.parametrize("caminho", [
    None,                                   # Valor None
    "",                                     # String vazia
    " ",                                    # String com espaço em branco
    0,                                      # Inteiro
    0.5,                                    # Float
    [],                                     # Lista vazia
    ["caminho"],                            # Lista com string
    {},                                     # Dicionário vazio
    {"path": "caminho"},                    # Dicionário com chave "path"
    object(),                               # Instância de objeto
    lambda x: x,                            # Função lambda
    b"/home/usuario/projeto/",              # Byte string
    "/home/usuario/projeto/\x00",           # Caracteres nulos no caminho
    "C:/Users/usuario/projeto/\x00",        # Caracteres nulos no Windows
    "/caminho_invalido\\erro_misto/",       # Mistura de barras no Linux
    "C:/Users/usuario/projeto/tests/unit/"  # Uso de barra comum no Windows
])
def test_validar_caminho_excecoes(caminho):
    """Teste a validação de caminhos para entradas inválidas."""
    with pytest.raises(ValueError):
        validar_caminho(caminho)
