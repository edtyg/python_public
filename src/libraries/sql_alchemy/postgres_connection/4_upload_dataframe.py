"""
Uploads data in pandas dataframe to database
"""

import pandas as pd

from keys.api_personal.databases.postgres import PGSQL_UBUNTU_ADMIN, PGSQL_VM_ADMIN
from src.libraries.sql_alchemy.sqlalchemy_client import SqlAlchemyConnector


def uploading_data(client):
    """does a select query using"""

    data = {
        "symbol": ["BTCUSD", "ETHUSD"],
        "price": [70000, 3000],
        "time": ["123", "234"],
    }
    df_data = pd.DataFrame(data)
    print(df_data)

    with client.engine.connect() as conn:
        try:
            df_data.to_sql(
                "testing",
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
