import os


class ManipuladorDiretorio:
    def criar_diretorio(self, caminho: str):
        try:
            os.makedirs(caminho, exist_ok=False)
            return {"success": "Diretório criado com sucesso."}
        except FileExistsError:
            return {"error": "Diretório já existe."}
