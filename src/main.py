# src/main.py


"""
Módulo principal para inicialização do servidor da aplicação.

Este módulo é responsável por iniciar o servidor FastAPI. Ele importa a função
`iniciar_servidor` do módulo `infraestrutura.servidor` e a executa quando o
script é executado diretamente. Este arquivo serve como ponto de entrada para
a aplicação.
"""

from src.infraestrutura.servidor import iniciar_servidor

if __name__ == "__main__":
    """
    Ponto de entrada principal para iniciar o servidor.

    Se este script for executado diretamente, a função `iniciar_servidor` será
    chamada para inicializar o servidor da API. Isso permite que o servidor
    seja iniciado ao rodar o comando `python src/main.py`.
    """
    iniciar_servidor()
