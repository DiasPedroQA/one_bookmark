#  src/infra/db/settings/connection_test.py
import pytest
from sqlalchemy.exc import OperationalError
from src.infra.db.settings.connection import DBConnectionHandler


@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture que fornece uma conexão de banco de dados para os testes.
    Utiliza a string de conexão definida no arquivo .env,
    que deve estar configurada para usar SQLite em memória
    durante os testes.
    """
    return DBConnectionHandler()


def test_create_database_engine(db_connection):
    """
    Testa a criação da engine de conexão do banco de dados.
    Verifica se a engine é criada corretamente e se está funcional.
    """
    engine = db_connection.get_engine()
    assert engine is not None, "A engine do banco de dados não foi criada."


def test_engine_can_connect(db_connection):
    """
    Testa se a engine consegue se conectar ao banco de dados.
    Verifica se é possível estabelecer uma conexão sem erros.
    """
    engine = db_connection.get_engine()

    try:
        with engine.connect() as connection:
            fail_str = "Falha ao tentar conectar ao banco de dados."
            assert connection is not None, fail_str
    except OperationalError as e:
        pytest.fail(f"Falha ao tentar conectar ao banco de dados. Detalhes: {str(e)}")  # noqa: E501


def test_connection(db_connection):
    """
    Testa se a conexão com o banco de dados está funcionando corretamente.
    Verifica se é possível executar uma consulta simples.
    """
    assert db_connection.test_connection(), "Erro: Falha ao testar a conexão com o banco de dados. Verifique se o banco está acessível e configurado corretamente."  # noqa: E501
