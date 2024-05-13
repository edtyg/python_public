"""
postrgres database
dropping tables child class
"""
from postgres_client import PostgresConnector

from local_credentials.api_personal.databases.postgres import (
    PGSQL_UBUNTU_ADMIN,
    PGSQL_WINDOWS_ADMIN,
)


class DropTables(PostgresConnector):
    """inherits connector from parent class"""

    def drop_table(self, table_name: str):
        """dropping table"""

        query = f"""
        DROP TABLE IF EXISTS {table_name}
        """
        self.cursor.execute(query)
        print(f"Table {table_name} if exists, is dropped")


if __name__ == "__main__":
    client = DropTables(AFTERSHOCK_PC_MAIN_ADMIN_LOCAL)

    client.drop_table("ed_trades")
    client.close_connection()
