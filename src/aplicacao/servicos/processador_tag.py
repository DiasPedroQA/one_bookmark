# """
# Este módulo contém a classe ServicoTag, responsável por processar e sanitizar
# dados de tags HTML.

# A classe ServicoTag permite analisar as tags HTML, sanitizar seus dados e
# retornar uma lista de tags processadas com os atributos adequados, como
# 'tag_name', 'text_content', 'href', entre outros.

# Classes:
#     ServicoTag: Processa e sanitiza dados de tags HTML.

# Funções:
#     processar_tags: Processa uma lista de dados de tags e aplica sanitização
#     em atributos relevantes.
# """
# from typing import List, Dict, Any


# class ServicoTag:
#     """
#     A classe ServicoTag é responsável por processar tags HTML e sanitizar
#     os dados associados, removendo caracteres problemáticos sem afetar acentos.

#     Attributes:
#         sanitizar_func: Função que realiza a sanitização dos dados das tags.
#     """

#     def __init__(self, sanitizar_func: callable):
#         """
#         Inicializa a instância da classe ServicoTag com a função de sanitização.

#         Args:
#             sanitizar_func: Função que será utilizada para sanitizar os dados das tags.
#         """
#         self.sanitizar_func = sanitizar_func

#     def processar_tags(self, dados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """Processa uma lista de dados de tags e retorna uma lista de tags processadas.

#         Args:
#             dados: Uma lista de dicionários representando as tags a serem processadas.

#         Returns:
#             Uma lista de dicionários com as tags processadas.

#         Raises:
#             ValueError: Se um dicionário não contém as chaves necessárias.
#         """
#         resultado = []

#         for tag in dados:
#             # Verifica se a chave 'tag_name' está presente
#             if "tag_name" not in tag:
#                 raise ValueError("A tag deve conter a chave 'tag_name'.")

#             tag_processada = {
#                 "tag_name": self.sanitizar_func(tag["tag_name"]),  # Sanitiza 'tag_name'
#                 "text_content": self.sanitizar_func(
#                     tag.get("text_content", "")
#                 ),  # Sanitiza 'text_content'
#                 "href": tag.get("href"),  # Algumas tags podem não ter href
#                 "alt": self.sanitizar_func(tag.get("alt", "")),  # Sanitiza 'alt'
#                 "classe": self.sanitizar_func(tag.get("classe", "")),  # Sanitiza 'classe'
#                 "id": self.sanitizar_func(tag.get("id", "")),  # Sanitiza 'id'
#                 "charset": tag.get(
#                     "charset"
#                 ),  # charset pode ser opcional, sem sanitização
#             }
#             resultado.append(tag_processada)

#         return resultado
