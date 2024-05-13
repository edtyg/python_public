"""
Selecting Postgres Table
"""

import pandas as pd
from sqlalchemy import text

from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def select_table(client, query: str):
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
    Select * from binance_spot_ethusdt_1m
    limit 100
    """
    data = select_table(client, query)
    print(data)
