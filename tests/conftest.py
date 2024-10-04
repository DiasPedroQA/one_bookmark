#  tests/conftest.py

"""
Configuração de fixtures para testes com pytest.

Este módulo configura o ambiente de teste utilizando o banco de dados
SQLite em memória. Ele fornece duas fixtures:
- `db_engine`: Cria e gerencia uma conexão com o banco de dados.
- `db_session`: Gerencia a criação e encerramento de sessões para cada teste.
"""

import os
import sys
from typing import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from src.infra.db.settings.base import Base

# Adiciona o diretório src ao PYTHONPATH
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../src')))


@pytest.fixture(scope='module')
def db_engine() -> Generator[Engine, None, None]:
    """
    Fixture que cria uma conexão de teste com o banco de dados em memória.

    Esta função configura um banco de dados SQLite em memória, que será
    usado para testes. Ela cria as tabelas necessárias antes dos testes e
    remove-as ao final.

    Yields:
        Engine: A engine do SQLAlchemy conectada ao banco de dados em memória.
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    """
    Fixture que cria uma nova sessão de banco de dados para cada teste.

    Para cada teste, esta função cria uma nova conexão e uma transação.
    Ao final do teste, a transação é revertida e a conexão é fechada.

    Args:
        db_engine (Engine): A engine do SQLAlchemy criada pela fixture `db_engine`.

    Yields:
        Session: Uma nova sessão de banco de dados para ser usada nos testes.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    this_session = sessionmaker(bind=connection)
    session = this_session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
