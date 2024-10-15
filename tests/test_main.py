# pylint: disable=C0116, C0114, W0012, W0611
from typing import List
import pytest  # noqa: F401
from pytest_mock import MockerFixture
from src.main import Inicializador

caminhos_relativos_teste = ["../../../../Downloads"]


def test_processar_caminhos(
    caminhos_relativos_teste: List[str], mocker: MockerFixture
) -> None:
    # Arrange
    mock_processador = mocker.patch('src.main.ProcessadorCaminhos')
    inicializador = Inicializador(caminhos_relativos_teste)

    # Act
    inicializador.processar_caminhos()

    # Assert
    mock_processador.assert_called_once_with(caminhos_relativos_teste)
    mock_processador.return_value.processar_caminhos.assert_called_once()


def test_inicializador_init(caminhos_relativos_teste: List[str]) -> None:
    # Arrange
    inicializador = Inicializador(caminhos_relativos_teste)

    # Assert
    assert inicializador.caminhos == caminhos_relativos_teste
