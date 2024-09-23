import os


class ManipuladorArquivo:
    def criar_arquivo(self, caminho: str, conteudo: str):
        if os.path.exists(caminho):
            return {"error": "Arquivo já existe."}
        with open(caminho, 'w') as f:
            f.write(conteudo)
        return {"success": "Arquivo criado com sucesso."}
