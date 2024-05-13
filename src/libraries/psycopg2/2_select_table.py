"""
postrgres database
selecting tables child class
"""
import pandas as pd
import psycopg2 as pg
from postgres_client import PostgresConnector

from local_credentials.api_personal.databases.postgres import (
    PGSQL_UBUNTU_ADMIN,
    PGSQL_WINDOWS_ADMIN,
)


class SelectTables(PostgresConnector):
    """inherits connector from parent class"""

    def select_table(self, table_name: str):
        """selecting table from postgres database"""

        query = f"""
        SELECT * FROM {table_name}
        """

        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            col_names = [i.name for i in self.cursor.description]
            dataframe_table = pd.DataFrame(data, columns=col_names)
            print(f"selecting table = {table_name}")
            return dataframe_table
        except pg.errors.UndefinedTable as error:
            dataframe_table = pd.DataFrame()
            print(error)
            return dataframe_table

        # return dataframe_table


if __name__ == "__main__":
    client = SelectTables(AFTERSHOCK_PC_MAIN_ADMIN_LOCAL)

    table = client.select_table("ed_trades")
    print(table)

    client.close_connection()
