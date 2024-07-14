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
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            sql_query = text(query)
            result_proxy = connection.execute(sql_query)
            trans.commit()  # need to commit here
            results = result_proxy.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")

        df_results = pd.DataFrame(results)
        return df_results


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    # Select data from the table
    query = """
    SELECT create_hypertable('cme', 'column5', migrate_data => true)
    """

    data = set_hypertable(client, query)
    print(data)
