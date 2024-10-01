# tests/test_infra/test_db/arquivo_entity_test.py
import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from infra.db.entities.pasta_entity import EntidadePasta
from infra.db.entities.arquivo_entity import EntidadeArquivo
from infra.db.entities.arquivo_log_entity import ArquivoLogEntity


# Carregar as variáveis do .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture(scope="module")
def test_db_engine():
    """
    Fixture que cria uma engine do banco de dados para os testes.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """
    Fixture que cria uma nova sessão para o banco de dados a cada teste.
    """
    session_local = sessionmaker(bind=test_db_engine)
    session = session_local()
    yield session
    session.rollback()
    session.close()


# Testes para EntidadeArquivo
def test_create_arquivo_entity(test_db_session):
    """
    Testa a criação de uma entidade 'EntidadeArquivo'
    e verifica se os atributos são armazenados corretamente.
    """
    pasta = EntidadePasta(name="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    new_arquivo = EntidadeArquivo(
        pasta_id=pasta.id,
        nome_arquivo="exemplo.txt",
        extensao_arquivo="txt",
        tamanho_em_bytes=1024,
    )
    test_db_session.add(new_arquivo)
    test_db_session.commit()

    saved_arquivo = test_db_session.query(
        EntidadeArquivo
    ).first()

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
    # Criar um arquivo para relacionar
    test_arquivo = EntidadeArquivo(
        id=1,
        nome_arquivo='test_arquivo.txt',
        extensao_arquivo='txt',
        tamanho_em_bytes=100)
    test_db_session.add(test_arquivo)
    test_db_session.commit()

    arquivo_log = ArquivoLogEntity(
        arquivo_id=1,
        action='created',
        description='Arquivo criado')
    test_db_session.add(arquivo_log)
    test_db_session.commit()

    assert arquivo_log.id is not None
    assert arquivo_log.action == 'created'
    assert arquivo_log.description == 'Arquivo criado'
    assert arquivo_log.arquivo_id == 1


def test_arquivo_log_relationship(test_db_session):
    """Teste para verificar o relacionamento entre
    ArquivoLog e EntidadeArquivo."""
    arquivo_log = test_db_session.query(
        ArquivoLogEntity
    ).filter_by(
        arquivo_id=1
    ).first()
    assert arquivo_log.arquivo is not None
    assert arquivo_log.arquivo.nome_arquivo == 'test_arquivo.txt'
