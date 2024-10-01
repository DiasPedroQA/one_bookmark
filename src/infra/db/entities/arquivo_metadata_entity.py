from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


# Criação da base declarativa
Base = declarative_base()


class ArquivoMetaDataEntity(Base):
    """
    Representação da tabela 'tb_arquivo_metadata'.

    Atributos:
        id (int): Identificador único da metadata do arquivo.
        arquivo_id (int): Referência ao arquivo relacionado.
        author (str): Autor do arquivo.
        last_modified (datetime): Data e hora da última modificação do arquivo.
        created_by (str): Usuário ou sistema que criou o arquivo.
    """
    __tablename__ = "tb_arquivo_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    arquivo_id = Column(
        Integer, ForeignKey("tb_arquivos.id", ondelete="CASCADE"),
        nullable=False
    )
    author = Column(String(255), default="Desconhecido")
    last_modified = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now())
    created_by = Column(String(255), default="Sistema")

    # Relacionamento com a tabela ArquivoEntity
    arquivo = relationship("ArquivoEntity", back_populates="metadatas")

    def __repr__(self) -> str:
        return (
            f"ArquivoMetaDataEntity(id={self.id}, author='{self.author}', "
            f"last_modified={self.last_modified}, "
            f"created_by='{self.created_by}')"
        )
