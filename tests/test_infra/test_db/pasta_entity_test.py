import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from infra.db.entities.pasta_entity import EntidadePasta


@pytest.fixture(scope='module')
def db_session_module():
    """Fixture para criar um banco de dados em memória para testes."""
    engine = create_engine(os.getenv("DATABASE_URL"))
    # Usando SQLite em memória
    Base.metadata.create_all(engine)  # Cria todas as tabelas apenas uma vez
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    yield session  # Retorna a sessão para os testes

    session.close()
    Base.metadata.drop_all(engine)  # Limpa as tabelas apenas no final


def test_pasta_creation(db_session):
    """Teste para verificar a criação de uma EntidadePasta."""
    pasta = EntidadePasta(nome_pasta='Test Folder')
    db_session.add(pasta)
    db_session.commit()

    assert pasta.id is not None
    assert pasta.nome_pasta == 'Test Folder'
    assert pasta.is_excluido is False


def test_subpasta_relationship(db_session):
    """Teste para verificar o relacionamento entre pastas e subpastas."""
    parent_pasta = EntidadePasta(nome_pasta='Parent Folder')
    db_session.add(parent_pasta)
    db_session.commit()  # Commit necessário para gerar o id do mae

    subpasta = EntidadePasta(
        nome_pasta='Subpasta', parent_pasta_id=parent_pasta.id)

    db_session.add(subpasta)
    db_session.commit()

    # Verificando se a subpasta foi adicionada ao mae corretamente
    assert parent_pasta.subpastas
    assert subpasta in parent_pasta.subpastas
    assert subpasta.parent_pasta_id == parent_pasta.id


def test_pasta_deletion(db_session):
    """Teste para verificar a marcação de uma pasta como deletada."""
    pasta = EntidadePasta(nome_pasta='Folder to Delete')
    db_session.add(pasta)
    db_session.commit()

    # Marcar a pasta como deletada
    pasta.is_excluido = True
    db_session.commit()

    # Verificar se a pasta está marcada como deletada
    assert pasta.is_excluido is True
