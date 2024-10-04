#  src/infra/db/settings/connection.py

"""
Este módulo fornece a classe DBConnectionHandler para gerenciar a conexão com o banco de dados
usando SQLAlchemy e variáveis de ambiente definidas em um arquivo .env.
"""

import os
from typing import List, Any, Tuple
from dotenv import load_dotenv
from pymysql import OperationalError, ProgrammingError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class DBConnectionHandler:
    """Gerencia a conexão com o banco de dados,
    utilizando variáveis de ambiente para definir a string de conexão."""

    def __init__(self) -> None:
        """Inicializa o gerenciador de conexão do banco de dados."""
        load_dotenv()  # Carrega as variáveis do arquivo .env

        # Carrega a URL completa do banco de dados
        # a partir da variável DATABASE_URL
        connection_string = os.getenv("DATABASE_URL")
        if connection_string is None:
            raise ValueError("DATABASE_URL não está definida no arquivo .env")
        self.__connection_string: str = connection_string  # Tipo de conexão

        # Criação do engine de banco de dados com base na connection string
        self.__engine: Engine = self.__create_database_engine()
        self.session: Session | None = None  # Tipo da sessão

    def __create_database_engine(self) -> Engine:
        """Cria o engine de conexão com o banco de dados.

        Raises:
            ValueError: Se a string de conexão não for válida.

        Returns:
            Engine: O engine do banco de dados.
        """
        if not self.__connection_string:
            raise ValueError("A string de conexão não pode ser None")
        return create_engine(self.__connection_string)

    def get_engine(self) -> Engine:
        """Retorna o engine do banco de dados.

        Returns:
            Engine: O engine do banco de dados.
        """
        return self.__engine

    def commit(self) -> None:
        """Comita as alterações na sessão do banco de dados."""
        if self.session:
            self.session.commit()

    def execute_query(self, query: str) -> List[Tuple[Any]]:
        """Executa uma consulta SQL diretamente no
        banco de dados e retorna os resultados.

        Args:
            query (str): A consulta SQL a ser executada.

        Returns:
            List[Tuple[Any]]: Os resultados da consulta.
        """
        with self.__engine.connect() as connection:
            result = connection.execute(text(query))
            return [tuple(row) for row in result.fetchall()]

    def test_connection(self) -> bool:
        """Teste se a conexão com o banco de dados está funcionando.

        Returns:
            bool: True se a conexão for bem-sucedida, False caso contrário.
        """
        try:
            with self.__engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return result.fetchone() is not None
        except (OperationalError, ProgrammingError) as e:
            print(f"Erro ao testar conexão: {e}")
            return False

    def __enter__(self) -> 'DBConnectionHandler':
        """Inicia uma sessão de banco de dados, permitindo
        o uso com gerenciadores de contexto.

        Returns:
            DBConnectionHandler: A instância do gerenciador de conexão.
        """
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type: None, exc_val: None, exc_tb: Any) -> None:
        """Fecha a sessão de banco de dados ao sair
        do gerenciador de contexto."""
        if self.session:
            self.session.close()
