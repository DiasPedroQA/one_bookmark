# src/infrastructure/db_mysql/models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Arquivo(Base):
    __tablename__ = 'arquivos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_absoluto = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Arquivo(id={self.id}, nome_arquivo={self.nome_arquivo}, "
            f"caminho_absoluto={self.caminho_absoluto})>"
        )
