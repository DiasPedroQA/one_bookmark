import sqlite3


class DatabaseManager:
    def __init__(self, uri):
        self.connection = sqlite3.connect(uri)

    def execute_query(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()

    def close(self):
        self.connection.close()
