"""
Creates Postgres Table
"""

from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    FLOAT,
    INTEGER,
    TIMESTAMP,
    Column,
    MetaData,
    String,
    Table,
)

from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from src.projects.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def create_table_cme(client):
    """does a select query using pandas"""

    metadata = MetaData()
    Table(
        "CME_CF_BRR",
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


def create_table_binance(client, table_name):
    """does a select query using pandas"""

    metadata = MetaData()
    Table(
        table_name,
        metadata,
        Column("utc_datetime", TIMESTAMP),
        Column("id", BIGINT),
        Column("price", FLOAT),
        Column("qty", FLOAT),
        Column("quote_qty", FLOAT),
        Column("time", BIGINT),
        Column("is_buyer_maker", BOOLEAN),
        Column("is_best_match", BOOLEAN),
        Column("hour", INTEGER),
        Column("reference", String),
    )
    try:
        metadata.create_all(client.engine)
        print("Table created")
    except Exception as error:
        print(f"Error creating table: {error}")


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
    client.connect("postgres")

    table_name = "binance_spot_ethusdt_trades_ht"
    create_table_binance(client, table_name)
