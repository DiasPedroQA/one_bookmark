from sqlalchemy import create_engine, text


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "{}://{}:{}@{}:{}/{}".format(
            "mysql+pymysql",
            "root",
            "#R1040grau$",
            "localhost",
            "3306",
            "file_manager",
        )
        self.__engine = self.__create_database_engine()

    def __create_database_engine(self) -> None:
        return create_engine(self.__connection_string)

    def get_engine(self) -> None:
        return self.__engine

    def execute_query(self, query: str):
        with self.__engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()
