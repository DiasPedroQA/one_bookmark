# import logging
# import pytest
# from src.use_cases.folder_service import FolderService
# from domain.entidade_pasta import SQLTable_Pasta

# # Configuração do logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def test_create_folder_path_with_absolute_path(db) -> None:
#     logger.info("Iniciando teste: test_create_folder_path_with_absolute_path")

#     folder_service = FolderService()
#     folder = folder_service.create_folder_path(db, "/home/pedro-pm-dias/Downloads")

#     logger.info("Objeto SQLTable_Pasta criado: {folder}")

#     # Confirme se o objeto foi criado corretamente e se a coluna path está correta
#     assert isinstance(folder, SQLTable_Pasta)
#     logger.info("ASSERT folder.path: %s", folder.path)
#     # assert folder.path == "/home/pedro-pm-dias/Downloads"
#     logger.info("Teste test_create_folder_path_with_absolute_path concluído com sucesso.")


# def test_create_folder_path_with_relative_path(db) -> None:
#     logger.info("Iniciando teste: test_create_folder_path_with_relative_path")

#     folder_service = FolderService()
#     folder = folder_service.create_folder_path(db, "Downloads")

#     logger.info("Objeto SQLTable_Pasta criado: %s", folder)

#     # Confirme se o caminho relativo foi aceito e armazenado
#     assert isinstance(folder, SQLTable_Pasta)
#     logger.info("ASSERT folder.path: %s", folder.path)
#     # assert folder.path == "Downloads"
#     logger.info("Teste test_create_folder_path_with_relative_path concluído com sucesso.")


# def test_invalid_folder_path(db) -> None:
#     logger.info("Iniciando teste: test_invalid_folder_path")
#     folder_service = FolderService()

#     # Testa se um ValueError é levantado ao tentar criar um caminho vazio
#     logger.info("Testando caminho vazio")
#     with pytest.raises(ValueError) as exc_info_empty:
#         folder_service.create_folder_path(db, "")
#     logger.info("Erro esperado: %s", exc_info_empty.value)

#     assert (
#         str(exc_info_empty.value)
#     ) == "O caminho da pasta não pode ser uma string vazia", (
#         f"Erro levantado com mensagem inesperada: {exc_info_empty.value}"
#     )

#     # Testa se um ValueError é levantado ao tentar criar um caminho com caracteres inválidos
#     logger.info("Testando caminho com caracteres inválidos")
#     with pytest.raises(ValueError) as exc_info_invalid_chars:
#         folder_service.create_folder_path(db, "/caminho/inválido/<>:*?|")
#     logger.info("Erro esperado: %s", exc_info_invalid_chars.value)

#     assert str(exc_info_invalid_chars.value) == (
#         "O caminho da pasta contém caracteres inválidos"
#     ), f"Erro levantado com mensagem inesperada: {exc_info_invalid_chars.value}"

#     # Testa se um ValueError é levantado ao tentar criar um caminho muito longo
#     long_path = "a" * 256  # Um exemplo de caminho muito longo
#     logger.info("Testando caminho muito longo")
#     with pytest.raises(ValueError) as exc_info_long_path:
#         folder_service.create_folder_path(db, long_path)
#     logger.info("Erro esperado: %s", exc_info_long_path.value)

#     assert str(exc_info_long_path.value) == (
#         "O caminho da pasta é muito longo"
#     ), f"Erro levantado com mensagem inesperada: {exc_info_long_path.value}"

#     # # Testa se um ValueError é levantado para caminhos que não são strings
#     # logger.info("Testando caminho que não é uma string")
#     # with pytest.raises(ValueError) as exc_info_non_string_path:
#     #     folder_service.create_folder_path(db, '12345')
#     # logger.info("Erro esperado: %s", exc_info_non_string_path.value)

#     # assert str(exc_info_non_string_path.value) == (
#     #     "O caminho da pasta deve ser uma string"
#     # ), f"Erro levantado com mensagem inesperada: {exc_info_non_string_path.value}"
#     # logger.info("Teste test_invalid_folder_path concluído com sucesso.")
