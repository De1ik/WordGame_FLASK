import mysql.connector

class UseDb:
    def __init__(self, config) -> None:
        self.configuration = config

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.configuration)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
        self.cursor.close()