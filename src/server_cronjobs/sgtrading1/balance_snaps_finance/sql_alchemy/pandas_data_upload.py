import pandas as pd
import yfinance as yf
from sqlalchemy_client import SqlAlchemyConnector

# things to note
# last row may not be latest data


def sql_importer(symbol: str, start_date: str, end_date: str):
    df = yf.download(symbol, start=start_date, end=end_date)

    try:
        df_db = pd.read_sql(symbol, conn_sqlalchemy.engine)  # read table 'AAPL'
        max_date = str(max(df_db["Date"]))  # get latest row from your current database
    except:
        max_date = start_date  # if db doesnt exist then take the start date

    new_rows = df[df.index > max_date]
    new_rows.to_sql(symbol, conn_sqlalchemy.engine, if_exists="append")

    print(f"{str(len(new_rows))} added to database")


if __name__ == "__main__":
    sql_importer("AAPL", "2022-12-01", "2023-2-19")
