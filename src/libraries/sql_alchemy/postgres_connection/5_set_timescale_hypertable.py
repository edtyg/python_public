"""
Sets up timescale db hypertable - must be installed
sets up on an existing table
table should not have a primary key
"""

import pandas as pd
from sqlalchemy import text

from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def set_hypertable(client, query: str):
    """Selects table using SQL Query"""

    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    results = result_proxy.fetchall()

    df_results = pd.DataFrame(results)
    return df_results


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    # Select data from the table
    query = """
    SELECT create_hypertable('binance_spot_ethusdt_1m', 'utc_datetime')
    """
    print(query)
    data = set_hypertable(client, query)
    print(data)
