"""
postrgres database
creating tables child class
"""
import psycopg2 as pg
from postgres_client import PostgresConnector

from local_credentials.api_personal.databases.postgres import (
    PGSQL_UBUNTU_ADMIN,
    PGSQL_WINDOWS_ADMIN,
)


class CreateTables(PostgresConnector):
    """inherits connector from parent class"""

    def create_table_trades(self):
        """creates table for trades"""
        table_name = "ed_trades"

        query = f"""
        CREATE TABLE {table_name} (
            id BIGINT PRIMARY KEY,
            time TIMESTAMPTZ NOT NULL,
            market VARCHAR(50),
            baseCurrency VARCHAR(10),
            quoteCurrency VARCHAR(10),
            side VARCHAR(10),
            size FLOAT,
            fee FLOAT,
            feeCurrency VARCHAR(10)
            )
        """
        try:
            self.cursor.execute(query)
            print(f"table {table_name} created")
        except pg.DatabaseError as error:
            print(error)

    def create_table_limit_orders(self):
        "creates table for limit orders"
        table_name = "client_limit_orders"

        query = f"""
        CREATE TABLE {table_name} (
            utc_datetime TIMESTAMPTZ NOT NULL,
            client VARCHAR(50) NOT NULL,
            client_side VARCHAR(10),
            pair VARCHAR(10),
            amount FLOAT,
            price FLOAT,
            base_ccy VARCHAR(10),
            quote_ccy VARCHAR(10),
            base_ccy_proceeds_expected FLOAT,
            quote_ccy_proceeds_expected FLOAT,
            placed_in VARCHAR(20),
            unique_id VARCHAR(100) PRIMARY KEY
            )
        """

        try:
            self.cursor.execute(query)
            print(f"table {table_name} created")
        except pg.DatabaseError as error:
            print(error)


if __name__ == "__main__":
    client = CreateTables(PGSQL_UBUNTU_ADMIN)

    client.create_table_trades()
    client.close_connection()
