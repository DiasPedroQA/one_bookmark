# src/interface/schemas/arquivo_schema.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ArquivoEntity(Base):
    __tablename__ = 'tb_arquivos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String, nullable=False)
    id_pasta = Column(Integer, ForeignKey('tb_pastas.id'))
    # Chave estrangeira para Pasta
    metadatas = relationship("ArquivoMetadataEntity", back_populates="arquivo")
    # Relacionamento com ArquivoMetadata
    logs = relationship("ArquivoLogEntity", back_populates="arquivo")
    # Relacionamento com ArquivoLog


class PastaEntity(Base):
    __tablename__ = 'tb_pastas'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    id_pasta_mae = Column(Integer, ForeignKey('tb_pastas.id'))
    # Chave estrangeira para Pasta mãe
    arquivos = relationship("ArquivoEntity", back_populates="pasta")
    # Relacionamento com EntidadeArquivo
    subpastas = relationship("PastaEntity", back_populates="pasta_mae")
    # Relacionamento com subpastas
    pasta_mae = relationship(
        "PastaEntity", remote_side=[id],
        back_populates="subpastas")
    # Relação de hierarquia


class ArquivoLogEntity(Base):
    __tablename__ = 'tb_arquivo_log'

    id = Column(Integer, primary_key=True)
    id_arquivo = Column(Integer, ForeignKey('tb_arquivos.id'))
    # Chave estrangeira para EntidadeArquivo
    acao = Column(String, nullable=False)
    # Ação realizada (criação, edição, exclusão)
    timestamp = Column(DateTime, nullable=False)
    # Data e hora da ação
    arquivo = relationship("ArquivoEntity", back_populates="logs")
    # Relacionamento com EntidadeArquivo


class ArquivoMetadataEntity(Base):
    __tablename__ = 'tb_arquivo_metadata'

    id = Column(Integer, primary_key=True)
    id_arquivo = Column(Integer, ForeignKey('tb_arquivos.id'))
    # Chave estrangeira para EntidadeArquivo
    chave = Column(String, nullable=False)
    # Chave do metadado
    valor = Column(String, nullable=False)
    # Valor do metadado
    arquivo = relationship("ArquivoEntity", back_populates="metadatas")
    # Relacionamento com EntidadeArquivo
