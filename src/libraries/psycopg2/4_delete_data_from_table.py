"""
postrgres database
delete data from tables - child class
"""
import psycopg2 as pg
from postgres_client import PostgresConnector

from local_credentials.api_personal.databases.postgres import (
    PGSQL_UBUNTU_ADMIN,
    PGSQL_WINDOWS_ADMIN,
)


class DeleteFromTables(PostgresConnector):
    """inherits connector from parent class"""

    def delete_table_data(self, table_name: str):
        """deletes all rows of data from existing table"""

        query = f"""
        DELETE FROM {table_name}
        """
        try:
            self.cursor.execute(query)
            print("data deleted from table = {table_name}")
        except pg.errors.UndefinedTable as error:
            print(error)


if __name__ == "__main__":
    client = DeleteFromTables(AFTERSHOCK_PC_MAIN_ADMIN_LOCAL)

    client.delete_table_data("ed_trades")
