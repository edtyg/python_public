"""
Postgres database - creating table
"""

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)

from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def create_table(client):
    """
    Creating table
    """

    table_name = "cme"
    metadata = MetaData()
    Table(
        table_name,
        metadata,
        Column("column1", String),
        Column("column2", Integer),
        Column("column3", BigInteger),
        Column("column4", Float),
        Column("column5", DateTime),
        Column("column6", Boolean),
    )
    try:
        metadata.create_all(client.engine)
        print("Table created")

    except Exception as error:
        print(f"Error creating table: {error}")


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    create_table_test(client)
