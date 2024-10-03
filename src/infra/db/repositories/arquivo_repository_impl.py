# src/infra/db/repositories/arquivo_repository_impl.py

from datetime import datetime
from src.infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.settings.connection import DBConnectionHandler


class ArquivoRepositorio:
    """
    Inserts a new file record into the database.

    Args:
        id_pasta (int): The ID of the folder the file belongs to.
        nome_arquivo (str): The name of the file.
        extensao_arquivo (str): The file extension.
        tamanho_arquivo_bytes (int): The size of the file in bytes.
        is_excluido (bool, optional): Indicates if the file has been deleted.
            Defaults to False.
        data_criacao (datetime, optional): The creation date of the file.
            If not provided, the current datetime is used.
        data_atualizacao (datetime, optional): The last update date of the
            file. If not provided, the current datetime is used.

    Returns:
        EntidadeArquivo: The newly created file record.

    Raises:
        ValueError: If there is an error inserting the file record.
    """
    @classmethod
    def inserir_arquivo(
        cls, id_pasta: int, nome_arquivo: str, extensao_arquivo: str,
        tamanho_arquivo_bytes: int, is_excluido: bool = False,
        data_criacao: datetime | None = None,
        data_atualizacao: datetime | None = None
            ) -> EntidadeArquivo:
        """
        Inserts a new file record into the database.

        Args:
            id_pasta (int): The ID of the folder the file belongs to.
            nome_arquivo (str): The name of the file.
            extensao_arquivo (str): The file extension.
            tamanho_arquivo_bytes (int): The size of the file in bytes.
            is_excluido (bool, optional): Indicates if the file has been
                deleted. Defaults to False.
            data_criacao (datetime, optional): The creation date of the file.
                If not provided, the current datetime is used.
            data_atualizacao (datetime, optional): The last update date of
                the file. If not provided, the current datetime is used.

        Returns:
            EntidadeArquivo: The newly created file record.

        Raises:
            ValueError: If there is an error inserting the file record.
        """
        if data_criacao is None:
            data_criacao = datetime.now()
        if data_atualizacao is None:
            data_atualizacao = datetime.now()

        novo_registro = None

        with DBConnectionHandler() as db_handler:
            try:
                novo_registro = EntidadeArquivo(
                    id_pasta=id_pasta,
                    nome_arquivo=nome_arquivo,
                    extensao_arquivo=extensao_arquivo,
                    tamanho_arquivo_bytes=tamanho_arquivo_bytes,
                    is_excluido=is_excluido,
                    data_criacao=data_criacao,
                    data_atualizacao=data_atualizacao)

                if db_handler.session is not None:
                    db_handler.session.add(novo_registro)
                    db_handler.session.commit()
                else:
                    raise ValueError(
                        "Sessão do banco de dados não está disponível.")

            except Exception as exception:
                if db_handler.session is not None:
                    db_handler.session.rollback()
                raise ValueError(
                    f"Erro ao inserir arquivo: {exception}") from exception

        return novo_registro
