from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, Boolean, Enum, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


# Criação da base declarativa
Base = declarative_base()


class ArquivoEntity(Base):
    """
    Representação da tabela 'tb_arquivos'.

    Atributos:
        id (int): Identificador único do arquivo.
        nome_arquivo (str): Nome do arquivo.
        id_pasta (int): ID da pasta à qual o arquivo pertence.
    """
    __tablename__ = 'tb_arquivos'

    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String, nullable=False)
    id_pasta = Column(Integer, ForeignKey('tb_pastas.id'))
    # Chave estrangeira para Pasta

    # Relacionamentos
    metadatas = relationship("ArquivoMetadataEntity", back_populates="arquivo")
    logs = relationship("ArquivoLogEntity", back_populates="arquivo")

    def __repr__(self) -> str:
        return (
            f"ArquivoEntity(id={self.id}, "
            f"nome_arquivo='{self.nome_arquivo}')"
        )


class EntidadeArquivo(Base):
    """
    Representação da tabela 'tb_arquivos'.

    Atributos:
        id_arquivo (int): Identificador único do arquivo.
        id_pasta (int): Referência à pasta à qual o arquivo pertence.
        nome_arquivo (str): Nome do arquivo.
        extensao_arquivo (str): Extensão do arquivo (txt, pdf, html, csv).
        tamanho_arquivo_bytes (int): Tamanho do arquivo em bytes.
        is_excluido (bool): Indica se o arquivo foi excluído.
        data_criacao (datetime): Data de criação do arquivo.
        data_atualizacao (datetime): Data da última atualização do arquivo.
    """
    __tablename__ = "tb_arquivos"
    __table_args__ = {'extend_existing': True}

    id_arquivo = Column(Integer, primary_key=True, autoincrement=True)
    id_pasta = Column(
        Integer, ForeignKey("tb_pastas.id", ondelete="CASCADE"),
        nullable=False)
    nome_arquivo = Column(
        String(255),
        nullable=False)
    extensao_arquivo = Column(
        Enum('txt', 'docx', 'pdf', 'html', 'csv', name='enum_file_extension'),
        nullable=False)
    tamanho_arquivo_bytes = Column(
        Integer, nullable=False, default=0)
    is_excluido = Column(
        Boolean,
        default=False)
    data_criacao = Column(
        TIMESTAMP,
        server_default=func.now())
    data_atualizacao = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now())

    # Relacionamento com a tabela EntidadePasta (tb_pastas)
    pasta = relationship("EntidadePasta")

    def __repr__(self) -> str:
        return (
            f"EntidadeArquivo(id_arquivo={self.id_arquivo}, "
            f"nome_arquivo='{self.nome_arquivo}', "
            f"extensao_arquivo='{self.extensao_arquivo}', "
            f"id_pasta={self.id_pasta})"
        )
