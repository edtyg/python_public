"""
SPOT execution program
"""
import pandas as pd
from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def tick_data(client):
    """
    Cancels spot order

    Args:
        client (_type_): binance spot client
    """
    df = pd.DataFrame()
    params = {
        "symbol": "BTCUSDT",
        "limit": 1000,
        "fromId": 3_612_380_000,
    }
    
    for i in range(50):
        
        data = client.get_old_trade_lookup(params)
        df_data = pd.DataFrame(data)
        from_id = df_data.tail(1)['id'].values[0]
        params["fromId"] = from_id
        df = pd.concat([df, df_data])
        print(df)
        
    return df


if __name__ == "__main__":

    tick_data = tick_data(spot_client_read)
    print(tick_data)
