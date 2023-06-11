"""
pip install mysql-connector-python
connecting to mysql server using
"""

import mysql.connector
from local_credentials.db_credentials import (
    AFTERSHOCK_PC_MAIN_LOCAL_MYSQL,
    AFTERSHOCK_PC_MINI_LOCAL_MYSQL,
)


class MysqlConnector:
    """initialize with connection credentials"""

    def __init__(self, credentials: dict):
        self.host = credentials["HOST"]
        self.database = credentials["DB"]
        self.user = credentials["USER"]
        self.port = credentials["PORT"]
        self.password = credentials["PASSWORD"]

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                port=self.port,
                password=self.password,
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print(f"connected to mysql database={self.host} with user={self.user}")
            self.list_all_tables()

        except TypeError:
            print("connection failed")

    def list_all_tables(self):
        """lists all tables in database"""

        query = f"""
        SELECT table_name
        FROM INFORMATION_SCHEMA.TABLES
        WHERE table_schema = '{self.database}'
        """

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(f"listing all tables in database = {self.database}")
        print(data)

    def close_connection(self):
        """close connection"""
        self.connection.close()
        print(f"connection to mysql database={self.host} with user={self.user} closed")


if __name__ == "__main__":
    client = MysqlConnector(AFTERSHOCK_PC_MINI_LOCAL_MYSQL)
    client.close_connection()
