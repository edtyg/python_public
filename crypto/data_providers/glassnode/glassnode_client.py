# -*- coding: utf-8 -*-
"""
API docs here
https://docs.glassnode.com/welcome-to-glassnode/readme
"""

import datetime as dt

import pandas as pd
import requests

from local_credentials.api_key_data import GLASSNODE_KEY_FREE


class GlassNode:
    """rest api for glassnode - crypto data"""

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "https://api.glassnode.com/"

    def get_exchange_flows(self, asset):
        # flow = inflow or outflow
        new_df = pd.DataFrame()

        endpoint = {
            "inflow": "v1/metrics/transactions/transfers_volume_to_exchanges_sum",
            "outflow": "v1/metrics/transactions/transfers_volume_from_exchanges_sum",
        }

        for i in endpoint:
            url = self.base_url + endpoint[i]

            date = dt.datetime.now()
            delta = dt.timedelta(hours=25)
            date_delta = date - delta
            ts = int(date_delta.timestamp())

            # current subscription allows only for day resolution
            params = {
                "api_key": self.api_key,
                "a": asset,
                "s": ts,
            }
            response = requests.request("GET", url, params=params)
            data = response.json()
            print(data)

            ts = []
            v = []

            for j in data:
                ts.append(
                    dt.datetime.fromtimestamp(j["t"]).strftime("%Y-%m-%d %H:%M:%S")
                )  # convert epoch time to string
                v.append(j["v"])

            dic = {"t": ts, "v": v}
            df = pd.DataFrame(dic)
            df.rename(columns={"t": "datetime", "v": "volume"}, inplace=True)
            df["flow_direction"] = i
            new_df = pd.concat([new_df, df])

        new_df = new_df.reset_index(drop=True)

        date = new_df.loc[0]["datetime"]
        vol = new_df.loc[0, "volume"] - new_df.loc[1, "volume"]
        flow_direction = "netflow"

        append_df = pd.DataFrame(
            {"datetime": date, "volume": vol, "flow_direction": flow_direction},
            index=[2],
        )
        new_df = pd.concat([new_df, append_df])
        new_df = new_df.round(2)

        return new_df


if __name__ == "__main__":
    client = GlassNode(GLASSNODE_KEY_FREE)
    flows = client.get_exchange_flows("BTC")
