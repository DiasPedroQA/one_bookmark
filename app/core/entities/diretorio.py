from typing import List, Union

from app.core.entities.arquivo import Arquivo


class Diretorio:
    def __init__(self, localizacao: str):
        self.localizacao = localizacao
        self.itens: List[Union[Arquivo, 'Diretorio']] = []

    def listar_itens(self) -> List[str]:
        return [item.nome for item in self.itens]

    def contar_itens(self) -> int:
        return len(self.itens)

    def adicionar_item(self, item: Union[Arquivo, 'Diretorio']) -> None:
        self.itens.append(item)

    def remover_item(self, nome: str) -> None:
        self.itens = [item for item in self.itens if item.nome != nome]
