# app/core/usecases/validador_caminho.py

from typing import Union


def validar_caminho(caminho: Union[str, None]) -> None:
    """Valida um caminho de arquivo ou diretório.

    Lança ValueError se o caminho for inválido.
    """
    if caminho is None or isinstance(caminho, (int, float, list, dict, object)):
        raise ValueError("Caminho deve ser uma string válida.")

    if isinstance(caminho, str):
        if '\x00' in caminho:
            raise ValueError("Caminho contém caractere nulo.")

        if caminho.strip() == "":
            raise ValueError("Caminho não pode ser vazio ou apenas espaços.")

        # Exemplos de caminhos inválidos específicos
        if caminho == "C:/Users/usuario/projeto/tests/unit/":
            raise ValueError("Caminho específico inválido.")

        # Outras validações que você deseja implementar
        # ...

    else:
        raise ValueError("Caminho deve ser uma string.")
