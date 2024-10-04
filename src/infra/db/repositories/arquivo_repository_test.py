# src/infra/db/repositories/arquivo_repository_test.py

"""
Módulo de testes para o repositório de arquivos. Este arquivo contém testes
para a inserção de arquivos no banco de dados e validações relacionadas.
"""

from datetime import datetime
from typing import Dict, Generator, Union
import pytest
from sqlalchemy.orm import Session
from src.infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.settings.connection import DBConnectionHandler
from .arquivo_repository_impl import ArquivoRepositorio


@pytest.fixture
def arquivo_data() -> Dict[str, Union[str, int, bool, datetime]]:
    """
    Fixture que fornece dados mockados para a entidade 'EntidadeArquivo'.

    Retorna:
        dict: Um dicionário contendo os dados simulados do arquivo.
    """
    return {
        'caminho_absoluto': '/caminho/para/exemplo_documento.html',
        'nome_arquivo': 'exemplo_documento',
        'extensao_arquivo': 'html',
        'tamanho_arquivo_bytes': 2048,
        'is_excluido': False,
        'data_criacao': datetime.now(),
        'data_atualizacao': datetime.now(),
    }


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Fixture que fornece uma sessão de banco de dados para os testes.

    Retorna:
        Generator[Session, None, None]: Um gerador que fornece uma sessão
        de banco de dados e garante o fechamento e limpeza ao final.
    """
    db_handler = DBConnectionHandler()
    with db_handler.get_engine().connect() as connection:
        session = Session(bind=connection)
        yield session  # Fornece a sessão para os testes
        session.query(EntidadeArquivo).delete()  # Limpa a tabela após o teste
        session.commit()


@pytest.fixture
def setup_arquivo(
    db_session: Session,
    arquivo_data: Dict[str, Union[str, int, bool, datetime]]
) -> None:
    """
    Testa a inserção de um arquivo no repositório.

    Args:
        db_session (Session): A sessão do banco de dados.
        arquivo_data (Dict[str, Union[str, int, bool, datetime]]): Os dados
        do arquivo a serem inseridos.
    """
    repositorio_arquivos = ArquivoRepositorio()

    # Verifica e converte o tamanho do arquivo
    file_tamanho_arquivo_bytes = (
        arquivo_data['tamanho_arquivo_bytes'] if isinstance(arquivo_data['tamanho_arquivo_bytes'], (int, float)) else 0
    )

    repositorio_arquivos.inserir_arquivo(
        file_caminho_absoluto=str(arquivo_data['caminho_absoluto']),
        file_nome=str(arquivo_data['nome_arquivo']),
        extensao_arquivo=str(arquivo_data['extensao_arquivo']),
        tamanho_arquivo_bytes=file_tamanho_arquivo_bytes,
        is_excluido=bool(arquivo_data['is_excluido']),
        data_criacao=arquivo_data['data_criacao'] if isinstance(arquivo_data['data_criacao'], datetime) else None,
        data_atualizacao=arquivo_data['data_atualizacao'] if isinstance(arquivo_data['data_atualizacao'], datetime) else None
    )

    # Verifica se o arquivo foi inserido corretamente
    arquivo_inserido = db_session.query(
        EntidadeArquivo
    ).filter_by(
        nome_arquivo=arquivo_data['nome_arquivo'],
        extensao_arquivo=arquivo_data['extensao_arquivo'],
        tamanho_arquivo_bytes=arquivo_data['tamanho_arquivo_bytes']
    ).first()

    assert arquivo_inserido is not None, "Erro: O arquivo não foi encontrado no banco de dados."
    assert arquivo_inserido.id_pasta == 2, f"Erro: ID da pasta esperado '2', mas encontrei: '{arquivo_inserido.id_pasta}'"
    assert arquivo_inserido.nome_arquivo == arquivo_data['nome_arquivo'], f"Erro: Nome esperado '{arquivo_data['nome_arquivo']}', mas encontrei: '{arquivo_inserido.nome_arquivo}'"
    assert arquivo_inserido.extensao_arquivo == arquivo_data['extensao_arquivo'], f"Erro: Extensão esperada '{arquivo_data['extensao_arquivo']}', mas encontrei: '{arquivo_inserido.extensao_arquivo}'"
    assert bool(arquivo_inserido.is_excluido) == arquivo_data['is_excluido'], f"Erro: Status esperado '{arquivo_data['is_excluido']}', mas encontrei: '{arquivo_inserido.is_excluido}'"
    assert arquivo_inserido.tamanho_arquivo_bytes == arquivo_data['tamanho_arquivo_bytes'], f"Erro: Tamanho esperado '{arquivo_data['tamanho_arquivo_bytes']}', mas encontrei: '{arquivo_inserido.tamanho_arquivo_bytes}'"
    assert arquivo_inserido.data_criacao == arquivo_data['data_criacao'], f"Erro: Data de criação esperada '{arquivo_data['data_criacao']}', mas encontrei: '{arquivo_inserido.data_criacao}'"
    assert arquivo_inserido.data_atualizacao == arquivo_data['data_atualizacao'], f"Erro: Data de atualização esperada '{arquivo_data['data_atualizacao']}', mas encontrei: '{arquivo_inserido.data_atualizacao}'"
