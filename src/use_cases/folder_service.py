# # Lógica de negócio para tratar caminho da pasta

# from domain.entidade_pasta import SQLTable_Pasta


# class FolderService:
#     def create_folder_path(self, db, path: str) -> SQLTable_Pasta:
#         try:
#             if not isinstance(path, str):
#                 raise ValueError("O caminho da pasta deve ser uma string")
#             if not path.strip():
#                 raise ValueError("O caminho da pasta não pode ser uma string vazia")
#             if any(char in path for char in '<>:*?|'):
#                 raise ValueError("O caminho da pasta contém caracteres inválidos")
#             if len(path) > 255:
#                 raise ValueError("O caminho da pasta é muito longo")

#             # Lógica de criação da pasta
#             folder: SQLTable_Pasta = SQLTable_Pasta(path=path)
#             db.add(folder)
#             db.commit()
#             db.refresh(folder)
#             return folder
#         except ValueError as e:
#             print(f"Erro ao criar caminho: {e}")
#             raise
