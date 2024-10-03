#  src/infra/db/settings/connection.py
import os
from dotenv import load_dotenv
from pymysql import OperationalError, ProgrammingError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    """Gerencia a conexão com o banco de dados,
    utilizando variáveis de ambiente para definir a string de conexão."""

    def __init__(self) -> None:
        load_dotenv()  # Carrega as variáveis do arquivo .env

        # Carrega a URL completa do banco de dados
        # a partir da variável DATABASE_URL
        self.__connection_string = os.getenv("DATABASE_URL")

        # Criação do engine de banco de dados com base na connection string
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        """Cria o engine de conexão com o banco de dados."""
        if not self.__connection_string:
            raise ValueError("A string de conexão não pode ser None")
        return create_engine(self.__connection_string)

    def get_engine(self):
        """Retorna o engine do banco de dados."""
        return self.__engine

    def commit(self):
        """Comita as alterações na sessão do banco de dados."""
        if self.session:
            self.session.commit()

    def execute_query(self, query: str):
        """Executa uma consulta SQL diretamente no
        banco de dados e retorna os resultados."""
        with self.__engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()

    def test_connection(self):
        """Teste se a conexão com o banco de dados está funcionando."""
        try:
            with self.__engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return result.fetchone() is not None
        except (OperationalError, ProgrammingError) as e:
            print(f"Erro ao testar conexão: {e}")
            return False

    def __enter__(self):
        """Inicia uma sessão de banco de dados, permitindo
        o uso com gerenciadores de contexto."""
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a sessão de banco de dados ao sair
        do gerenciador de contexto."""
        if self.session:
            self.session.close()
