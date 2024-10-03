#  src/infra/db/entities/arquivo_entity.py
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, Enum, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Criação da base declarativa
Base = declarative_base()


class EntidadeArquivo(Base):
    """
    Representação da tabela 'tb_arquivos' no banco de dados.

    Esta classe mapeia a tabela responsável por armazenar
    os arquivos no sistema.

    Atributos:
        id_arquivo (int): Identificador único do arquivo.
        id_pasta (int): Referência à pasta à qual o arquivo pertence.
        nome_arquivo (str): Nome do arquivo.
        extensao_arquivo (str): Extensão do arquivo
            (html, pdf, json, csv, txt, docx, etc.).
        tamanho_arquivo_bytes (int): Tamanho do arquivo em bytes.
        is_excluido (bool): Indica se o arquivo foi excluído.
        data_criacao (datetime): Data de criação do arquivo.
        data_atualizacao (datetime): Data da última atualização do arquivo.
    """
    __tablename__ = "tb_arquivos"

    id_arquivo = Column(Integer, primary_key=True, autoincrement=True)
    id_pasta = Column(
        Integer, ForeignKey("tb_pastas.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    nome_arquivo = Column(String(255), nullable=False)
    extensao_arquivo = Column(
        Enum('txt', 'docx', 'pdf', 'html', 'csv', name='enum_file_extension'),
        nullable=False
    )
    tamanho_arquivo_bytes = Column(Integer, nullable=False, default=0)
    is_excluido = Column(Boolean, default=False)
    data_criacao = Column(
        TIMESTAMP, server_default=func.now(),
        onupdate=func.now()
    )
    data_atualizacao = Column(
        TIMESTAMP, server_default=func.now(),
        onupdate=func.now()
    )

    # Relacionamento com a tabela EntidadePasta (tb_pastas)
    pasta = relationship(
        "EntidadePasta",
        back_populates="arquivos"
        )

    def __repr__(self) -> str:
        """
        Retorna uma representação em string da instância da classe.

        A representação inclui os atributos principais da entidade,
        permitindo fácil identificação e depuração.

        Returns:
            str: Representação em string da EntidadeArquivo.
        """
        return (
            f"EntidadeArquivo(id_arquivo={self.id_arquivo}, "
            f"nome_arquivo='{self.nome_arquivo}', "
            f"extensao_arquivo='{self.extensao_arquivo}', "
            f"id_pasta={self.id_pasta}, "
            f"tamanho_arquivo_bytes={self.tamanho_arquivo_bytes}, "
            f"is_excluido={self.is_excluido}, "
            f"data_criacao={self.data_criacao}, "
            f"data_atualizacao={self.data_atualizacao})"
        )

    def to_dict(self) -> dict:
        """
        Converte a instância da entidade em um dicionário.

        Isso pode ser útil para serialização e outras operações
        que requerem um formato de dicionário.

        Returns:
            dict: Representação da entidade como um dicionário.
        """
        return {
            "id_arquivo": self.id_arquivo,
            "id_pasta": self.id_pasta,
            "nome_arquivo": self.nome_arquivo,
            "extensao_arquivo": self.extensao_arquivo,
            "tamanho_arquivo_bytes": self.tamanho_arquivo_bytes,
            "is_excluido": self.is_excluido,
            # "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,  # noqa: E501
            # "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,  # noqa: E501
        }
