# tests/test_infra/test_db/arquivo_metadata_entity_test.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from infra.db.entities.arquivo_entity import EntidadeArquivo
from infra.db.entities.arquivo_metadata_entity import ArquivoMetaDataEntity


@pytest.fixture(scope='module')
def db_session():
    """Fixture para criar um banco de dados em memória para testes."""
    engine = create_engine('sqlite:///:memory:')  # Usando SQLite em memória
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    # Criando um arquivo para relacionar
    test_arquivo = EntidadeArquivo(
        id=1,
        nome_arquivo='test_arquivo.txt',
        extensao_arquivo='txt',
        tamanho_em_bytes=100
    )
    session.add(test_arquivo)
    session.commit()

    yield session  # Retorna a sessão para os testes

    session.close()
    Base.metadata.drop_all(engine)


def test_arquivo_metadata_creation(db_session):
    """Teste para verificar a criação de um ArquivoMetaDataEntity."""
    arquivo_metadata = ArquivoMetaDataEntity(
        arquivo_id=1, author='Pedro',
        created_by='Sistema'
    )
    db_session.add(arquivo_metadata)
    db_session.commit()

    assert arquivo_metadata.id is not None
    assert arquivo_metadata.author == 'Pedro'
    assert arquivo_metadata.created_by == 'Sistema'
    assert arquivo_metadata.arquivo_id == 1


def test_arquivo_metadata_relationship(db_session):
    """Teste para verificar o relacionamento entre
    ArquivoMetaDataEntity e EntidadeArquivo."""
    arquivo_metadata = db_session.query(
        ArquivoMetaDataEntity).filter_by(
            arquivo_id=1).first()

    assert arquivo_metadata.arquivo is not None
    assert arquivo_metadata.arquivo.nome_arquivo == 'test_arquivo.txt'
