# tests/conftest.py
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.db.settings.base import Base


# Adiciona o diretório src ao PYTHONPATH
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../src')))


@pytest.fixture(scope='module')
def db_engine():
    """Cria uma conexão de teste com o banco de dados."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(db_engine):
    """Cria uma nova sessão de banco de dados para cada teste."""
    connection = db_engine.connect()
    transaction = connection.begin()
    this_session = sessionmaker(bind=connection)
    session = this_session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
