# -*- coding: utf-8 -*-
"""
stablecoin_monitoring
to run this periodically and send message to telegram
if stablecoin prices exceed a certain range
"""

import pandas as pd
import requests
from python.sg1_server.cronjobs.risk_monitoring.telegram_client import Telegram

# self.chatgroup_hts_chatbot = "-987081068"  # hts chatbot with gongye
# self.market_information_test = "-990460215"  # main group for chat notifications


def main():
    """to check on stablecoin tickers"""
    list_of_symbols = ["USDCUSDT"]
    base_endpoint = "https://api.binance.com"
    endpoint = "/api/v3/ticker/price"
    lower_bound = 0.9990
    upper_bound = 1.0010

    df_price = pd.DataFrame()

    for symbol in list_of_symbols:
        response = requests.get(
            base_endpoint + endpoint, params={"symbol": symbol}, timeout=5
        )
        data = response.json()
        df_data = pd.DataFrame(data, index=[0])
        df_price = pd.concat([df_price, df_data])
    df_price["price"] = df_price["price"].astype("float")
    print(df_price)

    df_price_filtered = df_price.loc[
        ~df_price["price"].between(lower_bound, upper_bound)
    ]

    if df_price_filtered.empty:
        print("price within acceptable range")
    else:
        tg_client = Telegram()
        tg_chat = tg_client.market_information_test  # adjust chatgroup here
        telegram_format = df_price.to_string(index=False, header=True)

        tg_client.send_message(
            tg_chat,
            f"{tg_client.alarm_emoji*3} Binance Stablecoin Monitoring Alert {tg_client.alarm_emoji*3}",
        )
        tg_client.send_message(
            tg_chat,
            f"Acceptable range = [{lower_bound}, {upper_bound}]",
        )
        tg_client.send_message(
            tg_chat,
            telegram_format,
        )


if __name__ == "__main__":
    main()
