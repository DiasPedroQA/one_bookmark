# src/aplicacao/servicos/processador_caminhos.py

"""
Este módulo contém a classe `ProcessadorCaminhos`, que fornece
métodos para processar uma lista de caminhos, verificando se
cada caminho é um arquivo, uma pasta ou inválido, e realizando
as ações apropriadas para cada tipo de caminho.
"""

from pathlib import Path
from typing import List
from infraestrutura.helpers.logger import logaritmo

logger = logaritmo(__name__)


class ProcessadorCaminhos:
    """
    Inicializa a classe `ProcessadorCaminhos` com uma lista
    de caminhos a serem processados.

    Args:
        caminhos (List[str]): Uma lista de caminhos para processar.
    """

    def __init__(self, caminhos: List[str]) -> None:
        """
        Inicializa a classe com uma lista de caminhos.

        Args:
            caminhos: Uma lista de caminhos a serem processados.
        """
        self.caminhos: List[Path] = [Path(caminho) for caminho in caminhos]
        self.arquivos_encontrados: List[str] = []
        # Lista para armazenar arquivos processados

    def processar_caminhos(self) -> None:
        """
        Processa todos os caminhos fornecidos, verificando seu tipo
        e chamando os métodos apropriados para cada um.
        """
        for caminho in self.caminhos:
            if caminho.exists():
                if caminho.is_file():
                    self.processar_caminho_arquivo(caminho)
                elif caminho.is_dir():
                    self.processar_caminho_pasta(caminho)
            else:
                self.processar_caminho_invalido(caminho)

    def processar_caminho_arquivo(self, caminho: Path) -> None:
        """
        Processa um arquivo, realizando operações necessárias.

        Args:
            caminho: O caminho do arquivo a ser processado.
        """
        caminho_absoluto = caminho.resolve()  # Obtém o caminho absoluto
        logger.info("Arquivo: %s", caminho_absoluto)
        self.arquivos_encontrados.append(
            str(caminho_absoluto)
        )  # Armazena o caminho absoluto do arquivo

    def processar_caminho_pasta(self, caminho: Path) -> None:
        """
        Processa uma pasta, realizando operações necessárias.

        Args:
            caminho: O caminho da pasta a ser processada.
        """
        caminho_absoluto = caminho.resolve()  # Obtém o caminho absoluto
        logger.info("Pasta: %s", caminho_absoluto)
        # Processa cada item na pasta
        for item in caminho.iterdir():  # Usando iterdir() do pathlib
            logger.info("Item da pasta (%s): %s", caminho_absoluto, item.name)
            if item.is_file():
                self.processar_caminho_arquivo(item)  # Processa arquivo
            elif item.is_dir():
                self.processar_caminho_pasta(
                    item
                )  # Chama recursivamente para processar subpasta
            else:
                self.processar_caminho_invalido(item)  # Tratar itens inválidos se necessário

    def processar_caminho_invalido(self, caminho: Path) -> None:
        """
        Trata caminhos inválidos.

        Args:
            caminho: O caminho inválido a ser tratado.
        """
        logger.error("Caminho inválido: %s", caminho)

    def get_arquivos_encontrados(self) -> List[str]:
        """
        Retorna a lista de arquivos encontrados com seus caminhos absolutos.

        Returns:
            List[str]: Lista de caminhos absolutos dos arquivos processados.
        """
        return self.arquivos_encontrados
