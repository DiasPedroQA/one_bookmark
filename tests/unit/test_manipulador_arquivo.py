import pytest
from app.core.usecases.manipulador_arquivo import ManipuladorArquivo


def test_criar_arquivo():
    manipulador = ManipuladorArquivo()
    result = manipulador.criar('teste.txt', 'Conteúdo do teste')
    assert result is True  # ou outro critério de sucesso


def test_ler_arquivo():
    manipulador = ManipuladorArquivo()
    manipulador.criar('teste.txt', 'Conteúdo do teste')
    conteudo = manipulador.ler('teste.txt')
    assert conteudo == 'Conteúdo do teste'
