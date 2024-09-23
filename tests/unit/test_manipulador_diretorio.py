import os
import pytest
from app.core.usecases.manipulador_diretorio import ManipuladorDiretorio


@pytest.fixture
def manipulador_diretorio():
    return ManipuladorDiretorio()


def test_criar_diretorio_success(manipulador_diretorio):
    caminho = 'teste_diretorio'
    result = manipulador_diretorio.criar_diretorio(caminho)
    assert result['success'] == "Diretório criado com sucesso."
    assert os.path.exists(caminho)
    os.rmdir(caminho)


def test_criar_diretorio_existente(manipulador_diretorio):
    caminho = 'teste_diretorio_existente'
    os.mkdir(caminho)
    result = manipulador_diretorio.criar_diretorio(caminho)
    assert result['error'] == "Diretório já existe."
    os.rmdir(caminho)
