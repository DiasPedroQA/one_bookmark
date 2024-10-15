# src/main.py

"""
Este módulo contém a classe `Inicializador`, responsável por analisar e processar
uma lista de caminhos que podem ser arquivos ou diretórios. Ele utiliza a
classe `ProcessadorCaminhos` para manipular os caminhos fornecidos.
"""

from aplicacao.servicos.processador_caminhos import ProcessadorCaminhos


# pylint: disable=R0903  too-few-public-methods
class Inicializador:
    """
    A classe Inicializador é responsável por analisar e processar uma lista de caminhos.
    Ela utiliza a classe ProcessadorCaminhos para processar os caminhos fornecidos.
    """

    def __init__(self, caminhos: list[str]) -> None:
        """
        Inicializa a instância da classe Inicializador com uma lista de caminhos.

        Args:
            caminhos: Uma lista de strings representando os caminhos a serem processados.
        """
        self.caminhos = caminhos

    def processar_caminhos(self) -> None:
        """
        Inicia o processamento dos caminhos utilizando ProcessadorCaminhos.
        """
        processador = ProcessadorCaminhos(self.caminhos)
        processador.processar_caminhos()


# Exemplo de uso
if __name__ == "__main__":
    caminhos_relativos = [
        # "src",
        # "tests",
        # "pyproject.toml",
        # "README.md",
        # "requirements.in",
        # "requirements.txt",
        "../../../../Downloads"
    ]

    inicializador = Inicializador(caminhos_relativos)
    inicializador.processar_caminhos()
