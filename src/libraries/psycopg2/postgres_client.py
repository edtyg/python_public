"""
pip install psycopg2
connecting to postgresql server using psycopg2
"""

import psycopg2 as pg

from local_credentials.api_personal.databases.postgres import (
    PGSQL_UBUNTU_ADMIN,
    PGSQL_WINDOWS_ADMIN,
)


class PostgresConnector:
    """initialize with connection credentials"""

    def __init__(self, credentials: dict):
        self.host = credentials["HOST"]
        self.database = credentials["DB"]
        self.user = credentials["USER"]
        self.port = credentials["PORT"]
        self.password = credentials["PASSWORD"]

        try:
            self.connection = pg.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                port=self.port,
                password=self.password,
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print(f"connected to pgsql database = {self.host} with user = {self.user}")
            self.list_all_tables()

        except pg.OperationalError:
            print("connection failed - psycopg2")

    def list_all_tables(self):
        """lists all tables in database"""

        query = """
        SELECT table_schema || '.' || table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema NOT IN ('pg_catalog', 'information_schema')
        """

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(f"listing all tables in database = {self.database}")
        print(data)

        return data

    def close_connection(self):
        """close connection"""
        self.connection.close()
        print(
            f"connection to pgsql database = {self.host} with user = {self.user} closed"
        )


if __name__ == "__main__":
    client = PostgresConnector(PGSQL_WINDOWS_ADMIN)
    client.close_connection()
