# tests/test_infra/test_db/arquivo_entity_test.py

"""
Teste das entidades 'EntidadeArquivo' e 'ArquivoLogEntity'.

Este módulo contém testes para verificar a criação e relacionamento
das entidades 'EntidadeArquivo' e 'ArquivoLogEntity'.
"""

import os
from typing import Generator
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from src.infra.db.settings.base import Base
from src.infra.db.entities.pasta_entity import EntidadePasta
from src.infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.entities.arquivo_log_entity import ArquivoLogEntity

# Carregar as variáveis do .env
load_dotenv()


@pytest.fixture(scope="module")
def test_db_engine() -> Generator[Engine, None, None]:
    """
    Fixture que cria uma engine do banco de dados para os testes.

    Esta função cria uma engine de banco de dados com base na URL
    fornecida nas variáveis de ambiente e cria as tabelas necessárias.

    Yields:
        Engine: A engine do banco de dados para uso nos testes.

    Raises:
        ValueError: Se a variável de ambiente DATABASE_URL não estiver definida.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        raise ValueError("DATABASE_URL não está definido nas variáveis de ambiente.")

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Cria as tabelas no banco de dados
    yield engine
    engine.dispose()  # Fecha a conexão após os testes


@pytest.fixture(scope="function")
def test_db_session(test_db_engine: Engine) -> Generator[Session, None, None]:
    """
    Fixture que cria uma nova sessão para o banco de dados a cada teste.

    Esta função cria uma nova sessão de banco de dados para cada teste
    e garante que os dados sejam revertidos após a execução.

    Yields:
        Session: A sessão do banco de dados para uso nos testes.
    """
    session_local = sessionmaker(bind=test_db_engine)
    session = session_local()
    try:
        yield session
    finally:
        session.rollback()  # Faz rollback para limpar o banco após cada teste
        session.close()


# Testes para EntidadeArquivo
def test_create_arquivo_entity(test_db_session: Session) -> None:
    """
    Testa a criação de uma entidade 'EntidadeArquivo'.

    Este teste adiciona uma nova pasta e um novo arquivo ao banco de dados
    e verifica se a entidade foi criada corretamente.

    Args:
        test_db_session (Session): A sessão do banco de dados para o teste.
    """
    pasta = EntidadePasta(nome_pasta="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    novo_arquivo = EntidadeArquivo(
        file_nome="exemplo.txt",
        file_extensao="txt",
        file_tamanho=1024,
        file_caminho_absoluto="/caminho/para/exemplo.txt",
        file_is_deletado=False
    )
    test_db_session.add(novo_arquivo)
    test_db_session.commit()

    saved_arquivo = test_db_session.query(EntidadeArquivo).first()

    # Verificações
    assert saved_arquivo is not None, "Erro: A entidade 'EntidadeArquivo' não foi criada."
    assert saved_arquivo.id is not None, "Erro: O ID do arquivo não foi atribuído."
    assert saved_arquivo.nome_arquivo == "exemplo.txt", "Erro: Nome do arquivo não corresponde ao esperado."
    assert saved_arquivo.extensao_arquivo == "txt", "Erro: Extensão do arquivo não corresponde ao esperado."
    assert saved_arquivo.tamanho_arquivo_bytes == 1024, "Erro: Tamanho do arquivo não corresponde ao esperado."
    assert saved_arquivo.is_excluido is False, "Erro: O arquivo deve estar marcado como não excluído."
    assert saved_arquivo.pasta_id == pasta.id, "Erro: O ID da pasta não corresponde ao esperado."


# Testes para ArquivoLogEntity
def test_arquivo_log_creation(test_db_session: Session) -> None:
    """
    Teste para verificar a criação de um ArquivoLog.

    Este teste cria um novo arquivo e um log de criação associado
    e verifica se o log foi criado corretamente.

    Args:
        test_db_session (Session): A sessão do banco de dados para o teste.
    """
    test_arquivo = EntidadeArquivo(
        file_nome='test_arquivo.txt',
        file_extensao='txt',
        file_tamanho=100,
        file_caminho_absoluto='/caminho/absoluto/test_arquivo.txt',
        file_is_deletado=False
    )
    test_db_session.add(test_arquivo)
    test_db_session.commit()

    arquivo_log = ArquivoLogEntity(
        arquivo_id=test_arquivo.id,
        processo='created',
        description='Arquivo criado'
    )
    test_db_session.add(arquivo_log)
    test_db_session.commit()

    # Verificações
    assert arquivo_log.id is not None, "Erro: O ID do log de arquivo não foi atribuído."
    assert arquivo_log.processo.is_ == 'created', "Erro: O processo não corresponde ao esperado."
    assert arquivo_log.description.is_ == 'Arquivo criado', "Erro: A descrição do log não corresponde ao esperado."
    assert arquivo_log.arquivo_id == test_arquivo.id, "Erro: O ID do arquivo no log não corresponde ao esperado."


def test_arquivo_log_relationship(test_db_session: Session) -> None:
    """
    Teste para verificar o relacionamento entre ArquivoLog e EntidadeArquivo.

    Este teste cria um novo arquivo e um log de criação, e verifica
    se o log está corretamente associado ao arquivo.

    Args:
        test_db_session (Session): A sessão do banco de dados para o teste.
    """
    test_arquivo = EntidadeArquivo(
        file_nome='test_arquivo.html',
        file_extensao='html',
        file_tamanho=200,
        file_caminho_absoluto='/caminho/absoluto/test_arquivo.html',
        file_is_deletado=False
    )
    test_db_session.add(test_arquivo)
    test_db_session.commit()

    arquivo_log = ArquivoLogEntity(
        arquivo_id=test_arquivo.id,
        processo='created',
        description='Arquivo criado'
    )
    test_db_session.add(arquivo_log)
    test_db_session.commit()

    # Verificação com o ID correto
    log_retrieved = test_db_session.query(
        ArquivoLogEntity
    ).filter_by(
        arquivo_id=test_arquivo.id
    ).first()

    assert log_retrieved is not None, "Erro: O log de arquivo não foi encontrado."
    assert log_retrieved.arquivo.nome_arquivo == 'test_arquivo.html', "Erro: O nome do arquivo no log não corresponde ao esperado."
