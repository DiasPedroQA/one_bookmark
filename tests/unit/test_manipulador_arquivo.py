import os
import pytest
from app.core.usecases.manipulador_arquivo import ManipuladorArquivo


@pytest.fixture
def manipulador_arquivo():
    return ManipuladorArquivo()


def test_criar_arquivo_success(manipulador_arquivo):
    caminho = 'teste_arquivo.txt'
    conteudo = 'Conteúdo do arquivo.'
    result = manipulador_arquivo.criar_arquivo(caminho, conteudo)
    assert result['success'] == "Arquivo criado com sucesso."
    assert os.path.exists(caminho)

    with open(caminho, 'r') as f:
        assert f.read() == conteudo

    os.remove(caminho)


def test_criar_arquivo_existente(manipulador_arquivo):
    caminho = 'teste_arquivo_existente.txt'
    with open(caminho, 'w') as f:
        f.write('Arquivo existente.')

    result = manipulador_arquivo.criar_arquivo(caminho, 'Novo conteúdo')
    assert result['error'] == "Arquivo já existe."

    os.remove(caminho)
