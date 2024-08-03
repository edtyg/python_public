"""
Creating tables for binance klines
adjust for table names
"""

from sqlalchemy import (
    BIGINT,
    FLOAT,
    TIMESTAMP,
    Boolean,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    text,
)

from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from src.projects.postgres_database.connection_client import SqlAlchemyConnector


def create_table_binance(client, tablename: str):
    """Creating table"""

    metadata = MetaData()
    Table(
        tablename,
        metadata,
        Column("datetime", TIMESTAMP),
        Column("symbol", String),
        Column("trade_id", BIGINT),
        Column("price", FLOAT),
        Column("qty", FLOAT),
        Column("is_buyer_mm", Boolean),
    )

    try:
        metadata.create_all(client.engine)
        print(f"{tablename} Table created")

    except Exception as error:
        print(f"Error creating table: {error}")


def set_hypertable(client, tablename: str, datetime_col_name: str):
    """Selects table using SQL Query"""

    query = f"""
    SELECT create_hypertable('{tablename}', '{datetime_col_name}')
    """

    engine = client.engine
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            sql_query = text(query)
            result_proxy = connection.execute(sql_query)
            trans.commit()  # setting up hypertable
            results = result_proxy.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")

        df_results = pd.DataFrame(results)
        return df_results


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
    client.connect("postgres")

    # adjust table name and datetime column here
    table_name = "binance_spot_btcusdt_tick_data"
    dt_col_name = "utc_datetime"

    # creates table and sets up timescale hypertable
    create_table_binance(client, table_name)
    # set_hypertable(client, table_name, dt_col_name)
