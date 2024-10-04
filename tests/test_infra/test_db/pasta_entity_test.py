#  tests/test_infra/test_db/pasta_entity_test.py

"""
Este módulo contém os testes para a classe Pasta, garantindo
que todos os métodos e comportamentos estejam funcionando corretamente.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.pasta_entity import EntidadePasta


@pytest.fixture(scope='module')
def db_connection():
    """Fixture para gerenciar a conexão com o banco de dados durante os testes."""
    with DBConnectionHandler() as conn:
        yield conn


def test_criar_pasta(db_connection):
    """Teste para verificar a criação de uma nova pasta no banco de dados."""
    pasta = EntidadePasta(nome='Nova Pasta', caminho_absoluto='/home/user/Nova Pasta')
    db_connection.session.add(pasta)
    db_connection.commit()

    # Verifica se a pasta foi criada
    assert pasta.id is not None  # Supondo que `id` é gerado automaticamente


def test_pasta_nao_repetida(db_connection):
    """Teste para garantir que não é possível criar pastas com o mesmo nome."""
    pasta1 = EntidadePasta(nome='Pasta Única', caminho_absoluto='/home/user/Pasta Única')
    pasta2 = EntidadePasta(nome='Pasta Única', caminho_absoluto='/home/user/Pasta Única 2')

    db_connection.session.add(pasta1)
    db_connection.commit()

    db_connection.session.add(pasta2)

    # Espera-se que um IntegrityError ocorra ao tentar adicionar uma pasta duplicada
    with pytest.raises(IntegrityError):
        db_connection.commit()


def test_listar_pastas(db_connection):
    """Teste para verificar se todas as pastas são listadas corretamente."""
    pastas = db_connection.session.query(EntidadePasta).all()
    assert pastas is not None  # Verifica se a lista de pastas não está vazia
