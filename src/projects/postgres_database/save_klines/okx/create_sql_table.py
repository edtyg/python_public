"""
Creating tables for okx klines
adjust for table names
"""

from sqlalchemy import BIGINT, FLOAT, INTEGER, TIMESTAMP, Column, MetaData, Table, text

from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN
from src.projects.postgres_database.connection_client import SqlAlchemyConnector


def create_table_okx(client, tablename: str):
    """Creating table"""
    metadata = MetaData()
    Table(
        tablename,
        metadata,
        Column("utc_datetime", TIMESTAMP),
        Column("ts", BIGINT),
        Column("open", FLOAT),
        Column("high", FLOAT),
        Column("low", FLOAT),
        Column("close", FLOAT),
        Column("volume", FLOAT),
        Column("volccy", FLOAT),
        Column("volccyquote", FLOAT),
        Column("confirm", INTEGER),
    )
    try:
        metadata.create_all(client.engine)
        print(f"{table_name} Table created")
    except Exception as error:
        print(f"Error creating table: {error}")


def set_hypertable(client, tablename: str, datetime_col_name: str):
    """Selects table using SQL Query"""

    query = f"""
    SELECT create_hypertable('{tablename}', '{datetime_col_name}')
    """
    print(query)
    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    result = result_proxy.fetchall()
    print(result)


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    # adjust table name and datetime column here
    table_name = "okx_spot_ethusdt_1m"
    dt_col_name = "utc_datetime"

    # creates table and sets up timescale hypertable
    create_table_okx(client, table_name)
    set_hypertable(client, table_name, dt_col_name)
