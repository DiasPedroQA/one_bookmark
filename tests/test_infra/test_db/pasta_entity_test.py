# src/tests/test_pasta_repository.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from src.infra.db.entities.pasta_entity import EntidadePasta


@pytest.fixture(scope='module')
def db_session_module():
    """Fixture para criar um banco de dados em memória para testes."""
    # Usando SQLite em memória
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        raise ValueError("DATABASE_URL environment variable is not set")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Cria todas as tabelas apenas uma vez
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    yield session  # Retorna a sessão para os testes

    session.close()
    Base.metadata.drop_all(engine)  # Limpa as tabelas apenas no final


def test_pasta_creation(db_session_module):
    """Teste para verificar a criação de uma EntidadePasta."""
    pasta = EntidadePasta(nome_pasta='Test Folder')
    db_session_module.add(pasta)
    db_session_module.commit()

    assert pasta.id_pasta is not None
    assert pasta.nome_pasta.is_ == 'Test Folder'
    assert pasta.is_deleted.is_(False)


def test_subpasta_relationship(db_session_module):
    """Teste para verificar o relacionamento entre pastas e subpastas."""
    parent_pasta = EntidadePasta(nome_pasta='Parent Folder')
    db_session_module.add(parent_pasta)
    db_session_module.commit()  # Commit necessário para gerar o id do pai

    subpasta = EntidadePasta(
        nome_pasta='Subpasta', id_pasta_mae=parent_pasta.id_pasta
    )

    db_session_module.add(subpasta)
    db_session_module.commit()

    # Verificando se a subpasta foi adicionada ao pai corretamente
    assert parent_pasta.subpastas
    assert subpasta in parent_pasta.subpastas
    assert subpasta.id_pasta_mae.is_ == parent_pasta.id_pasta


def test_pasta_deletion(db_session_module):
    """Teste para verificar a marcação de uma pasta como deletada."""
    pasta = EntidadePasta(nome_pasta='Folder to Delete')
    db_session_module.add(pasta)
    db_session_module.commit()

    # Marcar a pasta como deletada
    pasta.is_deleted.is_(True)  # Verifique se 'is_deleted' é um Column
    db_session_module.commit()

    # Verificar se a pasta está marcada como deletada
    assert pasta.is_deleted.is_(True)
    # Recarregar a pasta do banco de dados para garantir
    # que a mudança foi persistida
    db_session_module.refresh(pasta)
    assert pasta.is_deleted.is_(True)
    # Verificar se a pasta não está mais presente na lista de subpastas
    assert pasta not in pasta.parent_pasta.subpastas
