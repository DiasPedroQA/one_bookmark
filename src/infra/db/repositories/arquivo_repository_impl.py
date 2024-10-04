#  src/infra/db/repositories/arquivo_repository_impl.py

"""
Módulo que contém a implementação do repositório de arquivos, responsável
por inserir e manipular registros de arquivos no banco de dados.
"""

from datetime import datetime
from infra.db.entities.arquivo_entity import EntidadeArquivo
from infra.db.settings.connection import DBConnectionHandler


class ArquivoRepositorio:
    """
    Classe que implementa o repositório de arquivos, permitindo a inserção
    e manipulação de registros no banco de dados.

    Métodos:
        inserir_arquivo: Insere um novo arquivo no banco de dados.
    """

    @classmethod
    def inserir_arquivo(
        cls,
        file_caminho_absoluto: str,
        file_nome: str,
        extensao_arquivo: str,
        tamanho_arquivo_bytes: int | None = 0,
        is_excluido: bool = False,
        data_criacao: datetime | None = None,
        data_atualizacao: datetime | None = None
    ) -> EntidadeArquivo:
        """
        Insere um novo registro de arquivo no banco de dados.

        Parâmetros:
            file_caminho_absoluto (str): O caminho absoluto do arquivo.
            file_nome (str): O nome do arquivo.
            extensao_arquivo (str): A extensão do arquivo.
            tamanho_arquivo_bytes (int): O tamanho do arquivo em bytes.
            is_excluido (bool, opcional): Indica se o arquivo foi excluído.
                O valor padrão é False.
            data_criacao (datetime, opcional): A data de criação do arquivo.
                Se não for fornecida, a data e hora atual serão usadas.
            data_atualizacao (datetime, opcional): A data de última atualização
                do arquivo. Se não for fornecida, a data e hora atual serão usadas.

        Retorna:
            EntidadeArquivo: O novo registro de arquivo criado.

        Levanta:
            ValueError: Se ocorrer um erro ao tentar inserir o arquivo no
            banco de dados.
        """

        # Garantindo que data_criacao e data_atualizacao tenham valores válidos
        data_criacao = data_criacao or datetime.now()
        data_atualizacao = data_atualizacao or datetime.now()

        # Garantindo que o novo_registro seja sempre instanciado corretamente
        novo_registro: EntidadeArquivo

        # Gerenciando a sessão do banco de dados
        with DBConnectionHandler() as db_handler:
            try:
                # Criação do novo registro de arquivo
                novo_registro = EntidadeArquivo(
                    file_caminho_absoluto=file_caminho_absoluto,
                    file_nome=file_nome,
                    file_extensao=extensao_arquivo,
                    file_tamanho=tamanho_arquivo_bytes,
                    file_is_deletado=is_excluido,
                    # file_data_criacao=data_criacao,
                    # file_data_modificacao=data_atualizacao
                )

                # Adicionando e 'commitando' o novo registro
                if db_handler.session:
                    db_handler.session.add(novo_registro)
                    db_handler.session.commit()
                else:
                    raise ValueError("Sessão do banco de dados não está disponível.")

            except (ValueError, TypeError) as exception:
                # Realiza rollback em caso de falha
                if db_handler.session:
                    db_handler.session.rollback()
                raise ValueError(f"Erro ao inserir arquivo '{file_nome}': {exception}") from exception
            except Exception as exception:
                # Trata outras exceções de forma genérica
                if db_handler.session:
                    db_handler.session.rollback()
                raise ValueError(f"Erro inesperado ao inserir arquivo: {exception}") from exception
            finally:
                # Garantindo que a sessão seja fechada após o uso
                if db_handler.session:
                    db_handler.session.close()

        return novo_registro
