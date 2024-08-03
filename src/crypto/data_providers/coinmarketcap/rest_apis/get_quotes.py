"""
Get coinmarketcap ohlcv
"""

import pandas as pd

from crypto.data_providers.coinmarketcap.rest_apis.user import cmc_user

if __name__ == "__main__":
    quotes = cmc_user.get_quotes_historical_v3(
        {
            "id": 13502,  # WLD
            "time_start": "2024-07-25",
            "time_end": "2024-07-30",
            "interval": "5m",
        }
    )
    print(quotes)

    # data = ohlcv["data"]["quotes"]
    # df_data = pd.DataFrame(data)
    # print(df_data)

    # for i in df_data.index:
    #     quote = df_data.loc[i, "quote"]["USD"]
    #     open_px = quote["open"]
    #     high_px = quote["high"]
    #     low_px = quote["low"]
    #     close_px = quote["close"]

    #     df_data.loc[i, "open"] = open_px
    #     df_data.loc[i, "high"] = high_px
    #     df_data.loc[i, "low"] = low_px
    #     df_data.loc[i, "close"] = close_px
