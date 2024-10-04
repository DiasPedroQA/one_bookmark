#  src/infra/db/entities/pasta_entity.py

from typing import List
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from infra.db.entities.arquivo_entity import EntidadeArquivo

# Criação da base declarativa
Base = declarative_base()


class EntidadePasta(Base):
    """
    Representação da tabela 'tb_pastas', que armazena as informações de pastas
    e diretórios do sistema.

    Atributos:
        id_pasta (int): Identificador único do diretório.
        nome_pasta (str): Nome do diretório.
        id_pasta_mae (Optional[int]): ID do diretório mãe, se houver.
        is_deleted (bool): Indica se o diretório foi excluído.
        data_criacao (datetime): Data e hora de criação do diretório.
        data_atualizacao (datetime): Data e hora da última modificação do diretório.
        subpastas (List['EntidadePasta']): Lista de subdiretórios (pastas filhas).
        arquivos (List['EntidadeArquivo']): Lista de arquivos associados ao diretório.
    """

    __tablename__ = 'tb_pastas'
    __table_args__ = {'extend_existing': True}

    id_pasta: Column[int] = Column(
        Integer,
        primary_key=True, autoincrement=True)
    nome_pasta: Column[str] = Column(
        String(55), nullable=False)
    id_pasta_mae: Column[int] = Column(
        Integer,
        ForeignKey('tb_pastas.id_pasta', ondelete="SET NULL"), nullable=True)
    is_deleted: Column[bool] = Column(
        Boolean, default=False)
    data_criacao: Column[datetime] = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
    data_atualizacao: Column[datetime] = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relacionamento para subdiretórios (pastas filhas)
    subpastas: Mapped[List["EntidadePasta"]] = relationship(
        "EntidadePasta",
        back_populates="pasta_mae",
        remote_side=[id_pasta]
    )    # Relacionamento com arquivos
    arquivos: Mapped[List["EntidadeArquivo"]] = relationship(
        "EntidadeArquivo",
        cascade="all, delete-orphan",
        back_populates="pasta"
    )

    def __repr__(self) -> str:
        """
        Retorna a representação em string da entidade pasta, útil para
        fins de depuração e logging.

        Returns:
            str: Representação textual do objeto EntidadePasta.
        """
        return (
            f"EntidadePasta(id_pasta={self.id_pasta}, "
            f"nome_pasta='{self.nome_pasta}', "
            f"id_pasta_mae={self.id_pasta_mae})"
        )
