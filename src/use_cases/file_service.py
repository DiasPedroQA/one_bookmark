# src/use_cases/file_service.py

import os
from sqlalchemy.orm import Session
from src.infrastructure.db.models import Arquivo


class FileService:
    def __init__(self, db: Session):
        self.db = db

    def criar_arquivo(self, nome_arquivo: str, caminho_absoluto: str, conteudo_html: str) -> Arquivo:
        # Cria o arquivo no sistema operacional
        with open(caminho_absoluto, 'w', encoding='utf-8') as f:
            f.write(conteudo_html)

        # Persiste no banco de dados
        novo_arquivo = Arquivo(nome_arquivo=nome_arquivo, caminho_absoluto=caminho_absoluto)
        self.db.add(novo_arquivo)
        self.db.commit()
        self.db.refresh(novo_arquivo)
        return novo_arquivo

    def buscar_arquivo_por_nome(self, nome_arquivo: str) -> Arquivo:
        return self.db.query(Arquivo).filter(Arquivo.nome_arquivo == nome_arquivo).first()

    def atualizar_arquivo(self, nome_arquivo: str, novo_conteudo_html: str) -> Arquivo:
        arquivo = self.buscar_arquivo_por_nome(nome_arquivo)
        if not arquivo:
            raise FileNotFoundError("Arquivo não encontrado")

        # Atualiza o arquivo no sistema operacional
        with open(str(arquivo.caminho_absoluto), 'w', encoding='utf-8') as f:
            f.write(novo_conteudo_html)

        # Aqui poderia adicionar lógica para atualizar no banco se necessário
        return arquivo

    def deletar_arquivo(self, nome_arquivo: str):
        arquivo = self.buscar_arquivo_por_nome(nome_arquivo)
        if not arquivo:
            raise FileNotFoundError("Arquivo não encontrado")

        # Deleta o arquivo do sistema operacional
        if os.path.exists(str(arquivo.caminho_absoluto)):
            os.remove(str(arquivo.caminho_absoluto))

        # Remove do banco de dados
        self.db.delete(arquivo)
        self.db.commit()
