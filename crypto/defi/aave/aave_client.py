import hmac
import datetime as dt
import requests
import hashlib
import pandas as pd


class aave:
    def __init__(self):
        self.base_url = "https://aave-api-v2.aave.com"

    def get_tvl(self):
        """
        https://aave-api-v2.aave.com/#/data/get_data_tvl

        GET - total value locked

        """

        endpoint = "/data/tvl"
        resp = requests.get(self.base_url + endpoint)
        data = resp.json()

        return data

    def get_vol(self):
        """
        https://aave-api-v2.aave.com/#/data/get_data_daily_volume_24_hours

        GET - 24 hours traded vol

        """

        endpoint = "/data/daily-volume-24-hours"
        resp = requests.get(self.base_url + endpoint)
        data = resp.json()

        return data

    def get_liquidity_v1(self, params: dict):
        """
        https://aave-api-v2.aave.com/#/data/get_data_liquidity_v1

        Args:
            params (dict):
            name    type    desc
            poolid  str     The id of the Aave Lending Pool Addresses Provider
            date    str     The date for where we want to get the data from 01-01-2020
        """

        endpoint = "/data/liquidity/v1"
        resp = requests.get(self.base_url + endpoint, params=params)
        data = resp.json()

        return data

    def get_liquidity_v2(self, params: dict):
        """
        https://aave-api-v2.aave.com/#/data/get_data_liquidity_v2

        Args:
            params (dict):
            name    type    desc
            poolid  str     The id of the Aave Lending Pool Addresses Provider
            date    str     The date for where we want to get the data from 01-01-2020
        """

        endpoint = "/data/liquidity/v2"
        resp = requests.get(self.base_url + endpoint, params=params)
        data = resp.json()

        return data

    def get_staking_pools(self):
        """
        https://aave-api-v2.aave.com/#/data/get_data_pools

        """

        endpoint = "/data/pools"
        resp = requests.get(self.base_url + endpoint)
        data = resp.json()

        return data


if __name__ == "__main__":
    client = aave()

    tvl = client.get_tvl()
    vol = client.get_vol()
    v1_liq = client.get_liquidity_v1(
        {"poolId": "0x24a42fd28c976a61df5d00d0599c34c4f90748c8"}
    )
    v2_liq = client.get_liquidity_v2(
        {"poolId": "0xb53c1a33016b2dc2ff3653530bff1848a515c8c5"}
    )
    pools = client.get_staking_pools()
