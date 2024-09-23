import pytest
from app.core.usecases.manipulador_diretorio import ManipuladorDiretorio


def test_criar_diretorio():
    manipulador = ManipuladorDiretorio()
    result = manipulador.criar('teste_diretorio')
    assert result is True  # ou outro critério de sucesso


def test_listar_diretorio():
    manipulador = ManipuladorDiretorio()
    manipulador.criar('teste_diretorio')
    items = manipulador.listar('teste_diretorio')
    assert isinstance(items, list)
