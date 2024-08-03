"""
Creates Postgres Table
"""

import pandas as pd
from sqlalchemy import text

from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from src.projects.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def set_hypertable(client, query: str):
    """sets hyper table"""

    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    results = result_proxy.fetchall()

    df_results = pd.DataFrame(results)
    return df_results


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
    client.connect("postgres")

    query = f"""
    SELECT create_hypertable('binance_spot_btcusdt_trades_ht', 'utc_datetime', chunk_time_interval => 86400)
    """

    table = set_hypertable(client, query)
    print(table)
