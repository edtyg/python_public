"""
making sql queries
"""
import os
import pandas as pd
import sqlalchemy
from connection_client import SqlAlchemyConnector


class SQLQueries(SqlAlchemyConnector):
    """inherits from SqlAlchemyConnector"""

    def __init__(self, credentials):
        super().__init__(credentials)
        self.postgres_connection()

    def create_table_sqlalchemy(self):
        """
        creating proof of reserve sql table
        """
        tablename = "exchange_por"

        query = sqlalchemy.text(
            f"""
            CREATE TABLE {tablename} (
            exchange VARCHAR(50),
            coin VARCHAR(20),
            final_balance FLOAT,
            date TIMESTAMP NOT NULL
            )
            """
        )
        try:
            self.connection.execute(query)
            print("Table created")
        except Exception as error:
            print(f"Error executing query: {error}")

    def select_table_por(self):
        """
        selecting proof of reserves table and return as dataframe
        can adjust sql query below
        """

        query = sqlalchemy.text(
            """
            SELECT * FROM exchange_por where date >= '2023-07-01'
            """
        )

        try:
            result = self.connection.execute(query).fetchall()
            df_result = pd.DataFrame(result)
            return df_result
        except Exception as error:
            print(f"Error executing query: {error}")

    def select_table_3pool(self):
        """
        selecting 3pool table and return as dataframe
        can adjust sql query below
        """

        query = sqlalchemy.text(
            """
            SELECT * FROM curve_3pool_monitor
            """
        )

        try:
            result = self.connection.execute(query).fetchall()
            df_result = pd.DataFrame(result)
            return df_result
        except Exception as error:
            print(f"Error executing query: {error}")


if __name__ == "__main__":
    SGTRD3_MARKETDATA_WRITE = {
        "HOST": "172.26.70.47",
        "DB": "marketdata",
        "USER": "postgres",
        "PORT": "5432",
        "PASSWORD": "postgres",
    }
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    output_excel_por = "exchange_por.xlsx"
    output_3pool = "curve_3pool.xlsx"

    writer_por = pd.ExcelWriter(save_path + output_excel_por)  # writer for xlsx files
    writer_3pool = pd.ExcelWriter(save_path + output_3pool)
    connector = SQLQueries(SGTRD3_MARKETDATA_WRITE)

    # selecting table
    df_por = connector.select_table_por()  # adjust sql query in row 47
    df_3pool = connector.select_table_3pool()  # selecting every row

    # will save data to excel file in same folder as this python file
    df_por.to_excel(writer_por, sheet_name="exchange_por", index=False)
    writer_por.close()
    print("por file saved")

    df_3pool.to_excel(writer_3pool, sheet_name="curve_3pool", index=False)
    writer_3pool.close()
    print("3pool file saved")
