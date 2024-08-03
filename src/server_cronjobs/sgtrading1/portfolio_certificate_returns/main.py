""" Calculates Yields for Spot vs Coin Margined Futures"""

import datetime as dt
import logging
import os

import pandas as pd

from helper.helper_config import ConfigHelper
from helper.helper_email import EmailHelper

### library files ###
from server_cronjobs.sgtrading1.portfolio_certificate_returns.binance_basis import (
    BinanceBasis,
    binance_instruments,
)
from server_cronjobs.sgtrading1.portfolio_certificate_returns.bybit_basis import (
    BybitBasis,
    bybit_instruments,
)
from server_cronjobs.sgtrading1.portfolio_certificate_returns.deribit_basis import (
    DeribitBasis,
    deribit_instruments,
)
from server_cronjobs.sgtrading1.portfolio_certificate_returns.kraken_client import (
    kraken,
)
from server_cronjobs.sgtrading1.portfolio_certificate_returns.okex_basis import (
    OkxBasis,
    okx_instruments,
)


def main():
    """
    Calculates Basis Yields
    """

    # took average of Spot and futures Taker Fees
    taker_fees_bps = {
        "Binance": 6.25,
        "Bybit": 2,
        "Okex": 1.5,
        "Deribit": 3.5,
    }

    # getting current time
    df_time = pd.DataFrame({"timesnap_hkt": [dt.datetime.now()]})

    # using spot prices from kraken
    client = kraken()
    btc_data = client.get_ohlc(params={"pair": "XBTUSD", "interval": 1440})
    eth_data = client.get_ohlc(params={"pair": "ETHUSD", "interval": 1440})

    btc_spot_price = float(btc_data["close"].values[-1])
    eth_spot_price = float(eth_data["close"].values[-1])

    btc_high_price = float(btc_data["high"].values[-1])
    eth_high_price = float(eth_data["high"].values[-1])

    btc_low_price = float(btc_data["low"].values[-1])
    eth_low_price = float(eth_data["low"].values[-1])

    df_spot_price = pd.DataFrame(
        {
            "Symbol": ["BTC_USD", "ETH_USD"],
            "Spot_Price": [
                round(float(btc_spot_price), 2),
                round(float(eth_spot_price), 2),
            ],
            "Spot_Price_High": [
                round(float(btc_high_price), 2),
                round(float(eth_high_price), 2),
            ],
            "Spot_Price_Low": [
                round(float(btc_low_price), 2),
                round(float(eth_low_price), 2),
            ],
        }
    )
    print(df_spot_price)

    ### pulling exchange futures data
    # binance data
    binance_df = BinanceBasis().get_list_highest_bids(binance_instruments)
    bybit_df = BybitBasis().get_list_highest_bids(bybit_instruments)
    okex_df = OkxBasis().get_list_highest_bids(okx_instruments)
    deribit_df = DeribitBasis().get_list_highest_bids(deribit_instruments)

    # combining the dataframes
    df = pd.concat([binance_df, bybit_df, okex_df, deribit_df], axis=0)

    # some adjustments to data
    df["price"] = df["price"].astype("float")

    df.loc[df["instrument"].str.startswith("BTC"), "underlying"] = (
        "BTC"  # creates underlying col
    )
    df.loc[df["instrument"].str.startswith("ETH"), "underlying"] = (
        "ETH"  # creates underlying col
    )

    df.loc[df["instrument"].str.startswith("BTC"), "spot_price"] = (
        btc_spot_price  # coinmarketcap spot price
    )
    df.loc[df["instrument"].str.startswith("ETH"), "spot_price"] = (
        eth_spot_price  # coinmarketcap spot price
    )

    df["spot_price"] = df["spot_price"].astype("float")

    def fees(x):
        fee_bps = taker_fees_bps[x]
        return fee_bps

    df["fees_bps"] = df["exchange"].apply(fees)

    df["futures_price_aft_fees"] = df["price"] * (1 - (df["fees_bps"] * 0.0001))
    df["days_to_expiry"] = (df["expiry"] - dt.datetime.now()).dt.days
    df["futures_expiry"] = df["expiry"].dt.strftime("%d %b %Y")

    df["24hr_vol_usd_million"] = round(df["vol_usd"], 2)
    df["indicative_net_returns_%"] = round(
        ((df["futures_price_aft_fees"] - df["spot_price"]) / df["spot_price"]) * 100, 2
    )
    df["indicative_net_returns_annualised_%"] = round(
        df["indicative_net_returns_%"] / df["days_to_expiry"] * 365, 2
    )
    df["indicative_net_returns_annualised_after_fees_%"] = round(
        df["indicative_net_returns_annualised_%"], 2
    )  # creates a copy
    df["indicative_net_returns_annualised_after_fees_%"] = [
        round(x * 0.8, 2) if x >= 0 else round(x, 2)
        for x in df["indicative_net_returns_annualised_after_fees_%"]
    ]
    # if -ve returns no need *0.8, if +ve returns * 0.8
    print(df)

    # df_final = selected columns
    df_final = df[
        [
            "exchange",
            "24hr_vol_usd_million",
            "instrument",
            "futures_expiry",
            "indicative_net_returns_%",
            "indicative_net_returns_annualised_%",
            "indicative_net_returns_annualised_after_fees_%",
        ]
    ]
    print(df_final)

    # save excel file
    writer = pd.ExcelWriter(save_path + filename)
    df_spot_price.to_excel(writer, sheet_name="spot_price")
    df_final.to_excel(writer, sheet_name="returns")
    writer.close()
    print("file Saved")

    return [df_time, df_spot_price, df_final]


if __name__ == "__main__":
    ### excel export ###
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    filename = "portfolio_certificate_returns.xlsx"

    ### logging ###
    logging.basicConfig(
        filename=save_path + "portfolio_cert.log",
        level=logging.INFO,  # set default to DEBUG - detailed info
        format="%(asctime)s:%(levelname)s:%(message)s",
        filemode="a",  # 'w' = write = create new file each time, 'a' = append = append each log
    )
    logger = logging.getLogger(__name__)
    ###############

    list_df = main()

    email_cred_config = "/home/edgar/python/config/others/emails/email_credentials.ini"
    email_recipients_config = (
        "/home/edgar/python/config/others/emails/email_recipients.ini"
    )

    email_config = ConfigHelper.get_section_data(email_cred_config, "otc_report")
    email_recipient = ConfigHelper.get_section_data(
        email_recipients_config, "portfolio_certificate"
    )
    print(list(email_recipient.values()))

    EmailHelper.send_email(
        email_user=email_config["username"],
        email_password=email_config["password"],
        email_recipients=list(email_recipient.values()),
        subject="Portfolio Certificate Returns",
        list_of_df=list_df,
        attachments_directory=save_path,
        list_of_attachments=[filename],
    )
