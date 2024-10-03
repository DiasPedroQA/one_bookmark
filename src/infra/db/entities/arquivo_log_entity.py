# src/infra/db/entities/arquivo_log_entity.py
from sqlalchemy import (
    Column, Integer, ForeignKey,
    Text, TIMESTAMP, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Criação da base declarativa
Base = declarative_base()


class ArquivoLogEntity(Base):
    """
    Representação da tabela 'tb_logs_arquivo', que armazena logs de ações
    realizadas em arquivos do sistema.

    Atributos:
        id (int): Identificador único do log.
        arquivo_id (int): Referência ao arquivo relacionado.
        processo (str): Ação realizada no arquivo
          (created, updated, deleted, restored).
        log_timestamp (datetime): Data e hora em que o log foi registrado.
        description (str): Descrição adicional do log, se houver.
    """
    __tablename__ = 'tb_logs_arquivo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    arquivo_id = Column(
        Integer,
        ForeignKey("tb_arquivos.id", ondelete="CASCADE"),
        nullable=False
    )
    processo = Column(
        Enum(
            'created', 'updated', 'deleted',
            'restored', name='enum_file_action'
        ),
        nullable=False
    )
    log_timestamp = Column(TIMESTAMP, server_default=func.now())
    description = Column(Text, nullable=True)

    # Relacionamento com a tabela EntidadeArquivo
    arquivo = relationship("EntidadeArquivo", back_populates="logs")

    def __repr__(self) -> str:
        return (
            f"ArquivoLogEntity(id={self.id}, processo='{self.processo}', "
            f"log_timestamp={self.log_timestamp}, "
            f"description='{self.description}')"
        )
