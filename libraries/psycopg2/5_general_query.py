"""
postrgres database
general query from database - child class
"""
import psycopg2 as pg
from postgres_client import PostgresConnector
from local_credentials.db_credentials import AFTERSHOCK_PC_MAIN_ADMIN_LOCAL


class GeneralQueries(PostgresConnector):
    """inherits connector from parent class"""

    def general_query(self):
        """general sql query"""

        query = """
        """

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data


if __name__ == "__main__":
    client = GeneralQueries(AFTERSHOCK_PC_MAIN_ADMIN_LOCAL)

    client.general_query()
    client.close_connection()
