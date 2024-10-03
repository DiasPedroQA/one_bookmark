# tests/conftest.py

import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base


# Adiciona o diretório src ao PYTHONPATH
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../src')))


@pytest.fixture(scope='module')
def db_engine():
    """Cria uma conexão de teste com o banco de dados em memória."""
    # Cria uma engine SQLite em memória
    engine = create_engine('sqlite:///:memory:')
    # Cria as tabelas no banco de dados
    Base.metadata.create_all(engine)
    # Retorna a engine para uso nos testes
    yield engine
    # Remove todas as tabelas após os testes
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(db_engine):
    """Cria uma nova sessão de banco de dados para cada teste."""
    connection = db_engine.connect()  # Conecta ao banco de dados
    transaction = connection.begin()  # Inicia uma transação
    this_session = sessionmaker(bind=connection)  # Cria um sessionmaker
    session = this_session()  # Cria uma nova sessão

    yield session  # Retorna a sessão para uso nos testes

    session.close()  # Fecha a sessão após os testes
    transaction.rollback()  # Reverte a transação
    connection.close()  # Fecha a conexão
