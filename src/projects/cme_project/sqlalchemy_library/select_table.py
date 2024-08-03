"""
Creates Postgres Table
"""

import pandas as pd
from sqlalchemy import text

from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from src.projects.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def select_table(client, query: str):
    """does a select query using"""

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

    query = """
    Select * from binance_spot_btcusdt_trades
    limit 100
    """

    table = select_table(client, query)
    print(table)
