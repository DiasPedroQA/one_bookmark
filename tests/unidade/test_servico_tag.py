# """
# Módulo de testes para o serviço de processamento de tags HTML e sanitização de texto.

# Este módulo contém testes para garantir o correto funcionamento do serviço
# `ServicoTag`, que processa tags HTML, e do sanitizador de texto, que remove
# caracteres Unicode problemáticos mantendo acentos e caracteres válidos.

# Fixtures:
#     - dados_tags: Retorna uma lista de dicionários representando diferentes
#         tipos de tags HTML usadas para testar o processamento de tags.
#     - dados_tags_com_acentos: Retorna uma lista de dicionários representando
#         tags HTML com acentos e caracteres especiais para testar a sanitização.

# Funções:
#     - assert_tag(tag, expected): Verifica se uma tag processada corresponde
#         aos valores esperados.
#     - test_sanitizar_texto(): Testa a função `sanitizar_texto` para garantir
#         que ela remova caracteres indesejados e mantenha acentos.
#     - test_processar_tags(dados_tags): Testa o método `processar_tags` do
#         `ServicoTag` para garantir que todas as tags sejam processadas
#         corretamente.
#     - test_processar_tags_com_sanitizacao(dados_tags_com_acentos): Testa o
#         processamento de tags que contém acentos e caracteres especiais,
#         verificando se a sanitização foi aplicada corretamente.
# """

# import pytest
# from aplicacao.servicos.processador_tag import ServicoTag
# from src.infraestrutura.helpers.sanitizador import sanitizar_texto


# @pytest.fixture
# def dados_tags():
#     """
#     Fixture que fornece uma lista de dicionários representando diferentes tags HTML.

#     Returns:
#         List[Dict[str, Any]]: Lista contendo dicionários com dados de tags HTML
#         como 'tag_name', 'href', 'text_content', etc.
#     """
#     return [
#         {
#             "tag_name": "A",
#             "href": "https://cheatsheets.zip/index.html",
#             "text_content": "CheatSheets.zip - Ultimate Cheat for Developers",
#         },
#         {"tag_name": "H3", "text_content": "Python"},
#         {
#             "tag_name": "A",
#             "href": "https://paulovasconcellos.com.br/10-bibliotecas-de-data-science-
# para-python-que-ninguém-te-conta-706ec3c4fcef",
#             "text_content": "10 bibliotecas de Data Science para Python que ninguém te conta",
#         },
#         {
#             "tag_name": "IMG",
#             "href": "https://example.com/imagem.png",
#             "alt": "Exemplo de Imagem",
#         },
#         {"tag_name": "P", "text_content": "Um parágrafo descritivo."},
#         {"tag_name": "DIV", "classe": "container", "id": "principal"},
#         {"tag_name": "BR"},
#         {"tag_name": "META", "charset": "UTF-8"},
#     ]


# @pytest.fixture
# def dados_tags_com_acentos():
#     """
#     Fixture que fornece uma lista de dicionários com tags HTML contendo acentos
#     e caracteres especiais.

#     Returns:
#         List[Dict[str, Any]]: Lista contendo dicionários com tags HTML
#         que possuem acentos e caracteres especiais, como 'tag_name' e 'text_content'.
#     """
#     return [
#         {
#             "tag_name": "A",
#             "href": "https://exemplo.com/paçoca",
#             "text_content": "Paçoca é um doce brasileiro",
#         },
#         {"tag_name": "P", "text_content": "São Paulo é uma cidade incrível!"},
#     ]


# def assert_tag(tag, expected):
#     """
#     Verifica se os atributos de uma tag correspondem aos valores esperados.

#     Args:
#         tag (Dict[str, Any]): O dicionário da tag processada.
#         expected (Dict[str, Any]): O dicionário com os valores esperados.

#     Raises:
#         AssertionError: Se algum valor da tag não corresponder ao esperado.
#     """
#     for key, value in expected.items():
#         assert tag.get(key) == value, str(
#             f"Falha na verificação da tag {tag['tag_name']}: "
#             f"esperava {key} = {value}, mas obteve {tag.get(key)}"
#         )


# def test_sanitizar_texto():
#     """
#     Testa a função sanitizar_texto para garantir que caracteres indesejados
#     sejam removidos corretamente, enquanto os acentos e caracteres válidos
#     sejam mantidos.
#     """
#     assert sanitizar_texto("Café") == "Café"
#     assert sanitizar_texto("naïve") == "naïve"
#     assert sanitizar_texto("Olá, mundo!") == "Olá, mundo!"
#     assert sanitizar_texto("São Paulo - Brasil!") == "São Paulo - Brasil!"
#     assert sanitizar_texto("Hello 😊!") == "Hello 😊!"  # Exemplo com emoji


# def test_processar_tags(dados_tags):
#     """
#     Testa o método processar_tags do ServicoTag para garantir que as tags
#     HTML sejam processadas corretamente.

#     Args:
#         dados_tags (List[Dict[str, Any]]): A fixture com os dados das tags HTML.

#     Raises:
#         AssertionError: Se o processamento das tags não corresponder ao esperado.
#     """
#     servico = ServicoTag()
#     resultado = servico.processar_tags(dados_tags)

#     # Verifica se todas as tags foram processadas
#     assert len(resultado) == len(dados_tags)

#     # Verifica as tags específicas
#     assert_tag(
#         resultado[0], {"tag_name": "A", "href": "https://cheatsheets.zip/index.html"}
#     )
#     assert_tag(resultado[1], {"tag_name": "H3", "text_content": "Python"})
#     assert_tag(
#         resultado[2],
#         {
#             "tag_name": "A",
#             "href": "https://paulovasconcellos.com.br/10-bibliotecas-de-data-science-
# para-python-que-ninguém-te-conta-706ec3c4fcef",
#         },
#     )
#     assert_tag(
#         resultado[3],
#         {
#             "tag_name": "IMG",
#             "href": "https://example.com/imagem.png",
#             "alt": "Exemplo de Imagem",
#         },
#     )
#     assert_tag(
#         resultado[4], {"tag_name": "P", "text_content": "Um parágrafo descritivo."}
#     )
#     assert_tag(
#         resultado[5], {"tag_name": "DIV", "classe": "container", "id": "principal"}
#     )
#     assert_tag(resultado[6], {"tag_name": "BR"})
#     assert_tag(resultado[7], {"tag_name": "META", "charset": "UTF-8"})


# def test_processar_tags_com_sanitizacao(dados_tags_com_acentos):
#     """
#     Testa o processamento de tags HTML que contém acentos e caracteres
#     especiais, verificando se a sanitização foi aplicada corretamente.

#     Args:
#         dados_tags_com_acentos (List[Dict[str, Any]]): A fixture com dados
#         das tags HTML que contêm acentos e caracteres especiais.

#     Raises:
#         AssertionError: Se o processamento das tags com sanitização não
#         corresponder ao esperado.
#     """
#     servico = ServicoTag()
#     resultado = servico.processar_tags(dados_tags_com_acentos)

#     # Verifica se a sanitização foi aplicada corretamente
#     assert_tag(
#         resultado[0],
#         {
#             "tag_name": "A",
#             "href": "https://exemplo.com/paçoca",
#             "text_content": "Paçoca é um doce brasileiro",
#         },
#     )
#     assert_tag(
#         resultado[1],
#         {"tag_name": "P", "text_content": "São Paulo é uma cidade incrível!"},
#     )
