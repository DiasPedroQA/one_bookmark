# src/infra/db/repositories/arquivo_repository_impl.py
from datetime import datetime
from infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.settings.connection import DBConnectionHandler


class ArquivoRepositorio:

    @classmethod
    def inserir_arquivo(
        cls, id_pasta: int, nome_arquivo: str,
        extensao_arquivo: str, tamanho_arquivo_bytes: int,
        is_excluido: bool, data_criacao: datetime,
        data_atualizacao: datetime
    ) -> None:
        with DBConnectionHandler() as database:
            try:
                novo_registro = EntidadeArquivo(
                    id_pasta=id_pasta,
                    nome_arquivo=nome_arquivo,
                    extensao_arquivo=extensao_arquivo,
                    tamanho_arquivo_bytes=tamanho_arquivo_bytes,
                    is_excluido=is_excluido,
                    data_criacao=data_criacao,
                    data_atualizacao=data_atualizacao)
                database.session.add(novo_registro)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
