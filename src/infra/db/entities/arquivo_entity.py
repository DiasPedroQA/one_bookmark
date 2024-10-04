#  src/infra/db/entities/arquivo_entity.py

import enum
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Criação da base declarativa
Base = declarative_base()


# Enum para representar as extensões de arquivo
class ExtensaoArquivoEnum(enum.Enum):
    CSV = 'csv'
    DOCX = 'docx'
    HTML = 'html'
    JSON = 'json'
    PDF = 'pdf'
    TXT = 'txt'


class EntidadeArquivo(Base):
    """
    Representação da tabela 'tb_files' no banco de dados.

    Esta classe mapeia a tabela responsável por armazenar
    os arquivos no sistema.
    """

    __tablename__ = 'tb_files'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_caminho_absoluto = Column(String(500), nullable=False)
    file_nome = Column(String(255), nullable=False)
    file_tamanho = Column(Integer, nullable=True)
    file_extensao = Column(String(10), nullable=True)  # Poderia usar ExtensaoArquivoEnum
    file_is_deletado = Column(Boolean, default=False)
    folder_id = Column(
        Integer, ForeignKey('tb_folders.folder_id', ondelete='CASCADE'), nullable=True)
    file_data_criacao = Column(TIMESTAMP, server_default=func.now())
    file_data_modificacao = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relacionamento com a tabela EntidadePasta (tb_folders)
    pasta = relationship("EntidadePasta", back_populates="arquivos", lazy="joined")

    def __init__(
        self, file_caminho_absoluto: str, file_nome: str, file_tamanho: Optional[int] = 0,
        file_extensao: Optional[str] = "", folder_id: Optional[int] = 0,
        file_is_deletado: bool = False
    ) -> None:
        """
        Inicializa uma nova instância da classe EntidadeArquivo.

        Parâmetros:
            file_caminho_absoluto (str): Caminho absoluto do arquivo.
            file_nome (str): Nome do arquivo.
            file_tamanho (int, opcional): Tamanho do arquivo em bytes. Padrão é None.
            file_extensao (str, opcional): Extensão do arquivo. Padrão é None.
            folder_id (int, opcional): ID da pasta à qual o arquivo pertence. Padrão é None.
            file_is_deletado (bool): Indica se o arquivo foi excluído. Padrão é False.
        """
        self.file_caminho_absoluto = file_caminho_absoluto
        self.file_nome = file_nome
        self.file_tamanho = file_tamanho
        self.file_extensao = file_extensao
        self.folder_id = folder_id
        self.file_is_deletado = file_is_deletado

    def __repr__(self) -> str:
        """
        Retorna uma representação em string da instância da classe.

        Returns:
            str: Representação em string da EntidadeArquivo.
        """
        return (
            f"EntidadeArquivo(file_id={self.file_id}, "
            f"file_nome='{self.file_nome}', "
            f"file_extensao='{self.file_extensao}', "
            f"file_caminho_absoluto='{self.file_caminho_absoluto}', "
            f"file_tamanho={self.file_tamanho}, "
            f"file_is_deletado={self.file_is_deletado}, "
            f"folder_id={self.folder_id}, "
            f"file_data_criacao={self.file_data_criacao}, "
            f"file_data_modificacao={self.file_data_modificacao})"
        )

    def to_dict(self) -> dict:
        """
        Converte a instância da entidade em um dicionário.

        Returns:
            dict: Representação da entidade como um dicionário.
        """
        return {
            "file_id": self.file_id,
            "file_caminho_absoluto": self.file_caminho_absoluto,
            "file_nome": self.file_nome,
            "file_tamanho": self.file_tamanho,
            "file_extensao": self.file_extensao,
            "file_is_deletado": self.file_is_deletado,
            "folder_id": self.folder_id,
            "file_data_criacao": self.file_data_criacao,
            "file_data_modificacao": self.file_data_modificacao,
        }
