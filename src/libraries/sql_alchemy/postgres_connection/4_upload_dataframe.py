"""
Uploads data in pandas dataframe to database
"""

import datetime as dt

import pandas as pd

from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def uploading_data(client):
    """does a select query using"""

    data = {
        "column1": ["BTCUSD", "ETHUSD"],
        "column2": [1, 2],
        "column3": [1000000, 2000000],
        "column4": [0.12, 0.13],
        "column5": [dt.datetime(2024, 1, 1, 0, 0, 0), dt.datetime(2024, 1, 2, 0, 0, 0)],
        "column6": [True, False],
    }
    df_data = pd.DataFrame(data)
    print(df_data)

    with client.engine.connect() as conn:
        try:
            df_data.to_sql(
                "cme",
                conn,
                if_exists="append",
                index=False,
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    uploading_data(client)
