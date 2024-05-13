"""
Postgres database - creating table
"""

from sqlalchemy import Column, Float, MetaData, String, Table

from keys.api_personal.databases.postgres import PGSQL_UBUNTU_ADMIN, PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def create_table_cme(client):
    """Creating table"""

    table_name = "cme"
    metadata = MetaData()

    cme_table = Table(
        table_name,
        metadata,
        Column("symbol", String),
        Column("rptSeq", String),
        Column("mdEntryType", String),
        Column("mdEntryPx", String),
        Column("mdEntryDate", String),
        Column("mdEntryTime", String),
        Column("mdUpdateAction", String),
        Column("openCloseSettlFlag", String),
        Column("netChgPrevDay", String),
        Column("netPctChg", String),
        Column("mdEntryCode", String),
    )
    try:
        metadata.create_all(client.engine)
        print("Table created")

    except Exception as error:
        print(f"Error creating table: {error}")


def create_table_testing(client):
    """Creating table"""

    table_name = "testing"
    metadata = MetaData()

    cme_table = Table(
        table_name,
        metadata,
        Column("symbol", String),
        Column("price", Float),
    )
    try:
        metadata.create_all(client.engine)
        print("Table created")

    except Exception as error:
        print(f"Error creating table: {error}")


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    # create_table_cme(client)
    # create_table_testing(client)
