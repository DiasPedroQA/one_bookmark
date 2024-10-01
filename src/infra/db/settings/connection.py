import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        load_dotenv()  # Carrega as variáveis do arquivo .env

        self.__connection_string = "{}://{}:{}@{}:{}/{}".format(
            os.getenv("DB_DRIVER"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self) -> None:
        return create_engine(self.__connection_string)

    def get_engine(self) -> None:
        return self.__engine

    def execute_query(self, query: str):
        with self.__engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()

    def __enter__(self):
        session_maked = sessionmaker(bind=self.__engine)
        self.session = session_maked()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()
