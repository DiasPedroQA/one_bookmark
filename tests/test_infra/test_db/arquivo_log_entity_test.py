# tests/test_infra/test_db/arquivo_entity_test.py

import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from src.infra.db.entities.pasta_entity import EntidadePasta
from src.infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.entities.arquivo_log_entity import ArquivoLogEntity

# Carregar as variáveis do .env
load_dotenv()


@pytest.fixture(scope="module")
def test_db_engine():
    """Fixture que cria uma engine do banco de dados para os testes."""
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        raise ValueError("DATABASE_URL environment variable is not set")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Cria as tabelas no banco de dados
    yield engine
    engine.dispose()  # Fecha a conexão após os testes


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Fixture que cria uma nova sessão para o banco de dados a cada teste."""
    session_local = sessionmaker(bind=test_db_engine)
    session = session_local()
    yield session
    session.rollback()  # Faz rollback para limpar o banco após cada teste
    session.close()


# Testes para EntidadeArquivo
def test_create_arquivo_entity(test_db_session):
    """Testa a criação de uma entidade 'EntidadeArquivo'."""
    pasta = EntidadePasta(nome_pasta="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    novo_arquivo = EntidadeArquivo(
        pasta_id=pasta.id,
        nome_arquivo="exemplo.txt",
        extensao_arquivo="txt",
        tamanho_em_bytes=1024,
    )
    test_db_session.add(novo_arquivo)
    test_db_session.commit()

    saved_arquivo = test_db_session.query(EntidadeArquivo).first()

    # Verificações
    assert saved_arquivo is not None
    assert saved_arquivo.id is not None
    assert saved_arquivo.nome_arquivo == "exemplo.txt"
    assert saved_arquivo.extensao_arquivo == "txt"
    assert saved_arquivo.tamanho_em_bytes == 1024
    assert saved_arquivo.is_excluido is False
    assert saved_arquivo.pasta_id == pasta.id


# Testes para ArquivoLogEntity
def test_arquivo_log_creation(test_db_session):
    """Teste para verificar a criação de um ArquivoLog."""
    test_arquivo = EntidadeArquivo(
        nome_arquivo='test_arquivo.txt',
        extensao_arquivo='txt',
        tamanho_em_bytes=100
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
    assert arquivo_log.id is not None
    assert arquivo_log.processo.in_ == 'created'
    assert arquivo_log.description.in_ == 'Arquivo criado'
    assert arquivo_log.arquivo_id == test_arquivo.id


def test_arquivo_log_relationship(test_db_session):
    """Teste para verificar o relacionamento entre
    ArquivoLog e EntidadeArquivo."""
    test_arquivo = EntidadeArquivo(
        nome_arquivo='test_arquivo.html',
        extensao_arquivo='html',
        tamanho_em_bytes=200
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
    log_retrieved = test_db_session.query(ArquivoLogEntity).filter_by(arquivo_id=test_arquivo.id).first()  # noqa: E501

    assert log_retrieved is not None
    assert log_retrieved.arquivo.nome_arquivo == 'test_arquivo.html'
