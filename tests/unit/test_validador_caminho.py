import pytest
from app.core.usecases.validador_caminho import validar_caminho


@pytest.mark.parametrize("caminho, esperado", [
    ("tests/unit/test_validador_caminho.py", 'arquivo'),
    ("tests/unit/", 'diretório'),
    ("caminho/nao/existe.txt", 'inexistente')
])
def test_validar_caminho(caminho, esperado):
    """Teste a criação da aplicação Flask.

    Verifica se a aplicação é criada corretamente e se as
    configurações essenciais estão configuradas corretamente
    no ambiente de desenvolvimento.
    """
    assert validar_caminho(caminho) == esperado
