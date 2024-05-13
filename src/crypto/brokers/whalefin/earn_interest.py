"""
calculates interest yields
using 1 day as tenor for customizable earn
"""

import pandas as pd
from earn_products_id import id_dict
from whalefin_rest_client import WhaleFin

from local_credentials.api_key_brokers import WHALEFIN_KEY, WHALEFIN_SECRET


def get_fixed_earn_products(whalefin_client):
    """get fixed earn products"""

    final_df = pd.DataFrame()
    name = [
        "Fixed Earn - BTC",
        "Fixed Earn - ETH",
        "Fixed Earn - USDⓈ",
        "Fixed Earn - USDT",
    ]

    for page in range(3):
        fixed_earn_products = whalefin_client.get_list_earn_products(
            {"type": "FIXED", "size": 20, "page": page + 1}
        )
        scraped_data = fixed_earn_products["result"]["items"]
        df_scraped_data = pd.DataFrame(scraped_data)
        final_df = pd.concat([final_df, df_scraped_data])

    df_fixed = final_df.loc[final_df["name"].isin(name)]
    df_fixed = df_fixed.sort_values(by=["ccy", "tenor"])
    df_fixed.reset_index(drop=True, inplace=True)

    df_fixed = df_fixed[["id", "name", "type", "ccy", "tenor", "originalApr"]]

    return df_fixed


def get_customizable_earn(whalefin_client):
    """get customizable tenor for earn"""

    final_df = pd.DataFrame()

    key_dict = id_dict  # from earn_products_id.py

    for item in key_dict.items():
        # item = ('BTC', '2XDAqZ4drwnytCbB46Ffe')
        custom_earn_products = whalefin_client.get_customized_earn_products(
            {
                "id": item[1],
                "tenor": 1,
            }
        )
        apr = custom_earn_products["result"]["apr"]

        new_dict = {
            "id": item[1],
            "name": f"Customized Earn - {item}",
            "type": "Customized",
            "ccy": item[0],
            "tenor": 1,
            "originalApr": apr,
        }

        df_new = pd.DataFrame(new_dict, index=[0])
        final_df = pd.concat([final_df, df_new])

    final_df.reset_index(drop=True, inplace=True)

    return final_df


def get_earn_yields(whalefin_client):
    """get yields"""

    fixed_products = get_fixed_earn_products(whalefin_client)
    custom_products = get_customizable_earn(whalefin_client)

    df_yield = pd.concat([fixed_products, custom_products])
    df_yield = df_yield.sort_values(by=["ccy", "tenor"])  # sort by multiple columns
    df_yield.reset_index(drop=True, inplace=True)

    df_yield["originalApr"] = df_yield["originalApr"].astype("float")
    df_yield["originalApr"] = df_yield["originalApr"] * 100
    df_yield.rename(columns={"originalApr": "apr %"}, inplace=True)
    df_yield["platform"] = "Whalefin"

    return df_yield


if __name__ == "__main__":
    client = WhaleFin(WHALEFIN_KEY, WHALEFIN_SECRET)

    df_combined = get_earn_yields(client)
