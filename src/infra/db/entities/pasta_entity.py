from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Criação da base declarativa
Base = declarative_base()


class PastaEntity(Base):
    """
    Representação da tabela 'tb_pastas'.

    Atributos:
        id (int): Identificador único da pasta.
        nome (str): Nome da pasta.
        id_pasta_mae (int): ID da pasta mãe, se houver.
    """
    __tablename__ = 'tb_pastas'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    id_pasta_mae = Column(Integer, ForeignKey('tb_pastas.id'))
    # Chave estrangeira para Pasta mãe

    # Relacionamentos
    arquivos = relationship(
        "ArquivoEntity",
        back_populates="pasta")
    subpastas = relationship(
        "PastaEntity",
        back_populates="pasta_mae")
    pasta_mae = relationship(
        "PastaEntity",
        remote_side=[id],
        back_populates="subpastas")

    def __repr__(self) -> str:
        return f"PastaEntity(id={self.id}, nome='{self.nome}')"


class EntidadePasta(Base):
    """
    Representação da tabela 'tb_pastas'.

    Atributos:
        id_pasta (int): Identificador único do diretório.
        nome_pasta (str): Nome do diretório.
        id_pasta_mae (int): ID do diretório mae, se houver.
        is_excluida (bool): Indica se o diretório foi excluído.
        data_criacao (datetime): Data e hora de criação do diretório.
        data_atualizacao (datetime): Data e hora da última
          modificação do diretório.
    """
    __tablename__ = 'tb_pastas'
    __table_args__ = {'extend_existing': True}

    id_pasta = Column(
        Integer,
        primary_key=True, autoincrement=True)
    nome_pasta = Column(
        String(
            55), nullable=False)
    id_pasta_mae = Column(
        Integer,
        ForeignKey('tb_pastas.id_pasta'), nullable=True)
    is_excluida = Column(
        Boolean,
        default=False)
    data_criacao = Column(
        TIMESTAMP,
        server_default='NOW()')
    data_atualizacao = Column(
        TIMESTAMP,
        server_onupdate='NOW()')

    # Relacionamentos para subdiretórios
    subpastas = relationship(
        'EntidadePasta',
        backref='pasta_mae',
        remote_side=[id_pasta]
    )

    def __repr__(self) -> str:
        return (
            f"EntidadePasta(id={self.id_pasta}, "
            f"nome_pasta='{self.nome_pasta}')"
        )
