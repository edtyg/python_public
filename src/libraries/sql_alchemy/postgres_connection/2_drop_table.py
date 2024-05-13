"""
Postgres database - dropping table
"""

from sqlalchemy import MetaData

from keys.api_personal.databases.postgres import PGSQL_UBUNTU_ADMIN, PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def drop_table_cme(client):
    """Dropping table"""

    table_name = "testing"
    metadata = MetaData()

    try:
        metadata.reflect(bind=client.engine)
        if table_name in metadata.tables:
            table = metadata.tables[table_name]
            table.drop(bind=client.engine)
            print("Table dropped")
        else:
            print("Table does not exist")
    except Exception as error:
        print(f"Error dropping table: {error}")


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    # Drop the table first
    drop_table_cme(client)
