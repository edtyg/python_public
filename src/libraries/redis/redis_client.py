"""
https://redis.io/docs/clients/python/
pip install redis

redis is a NoSQL database
data is stored as key-value pairs

uses RAM to store data
"""
import pickle
import zlib

import pandas as pd
import redis

from local_credentials.api_personal.databases.redis import REDIS_UBUNTU_ADMIN


class RedisClient:
    """
    Connection client to redis database
    """

    def __init__(self, connection_credentials: dict):
        self.redis_client = redis.Redis(
            host=connection_credentials["HOST"],
            port=connection_credentials["PORT"],
            password=connection_credentials["PASSWORD"],
            db=connection_credentials["DB"],
        )

    def redis_set(self, key: str, value: str):
        """sets a key value pair"""
        self.redis_client.set(key, value)

    def redis_get(self, key: str):
        """gets value by using key"""
        return self.redis_client.get(key)

    def redis_drop(self, redis_key: str):
        """deletes key:value pair by key"""
        self.redis_client.delete(redis_key)

    def redis_get_keys(self):
        """gets all keys"""
        return self.redis_client.keys()

    def set_key_value_dataframe(self, redis_key: str, redis_value: pd.DataFrame):
        """sets a new key-value pair where value is a pandas dataframe
        compresses data

        Args:
            redis_key (str): key i.e BINANCE_BTC_USDT_ORDERBOOK
            redis_value (_type_): value = pandas dataframe
        """
        value = zlib.compress(pickle.dumps(redis_value))
        self.redis_client.set(name=redis_key, value=value)

    def get_key_dataframe(self, redis_key: str):
        """gets value of specified redis_key whose
        value = pandas dataframe in this case

        Args:
            redis_key (str): key i.e BINANCE_BTC_USDT_ORDERBOOK
            redis_value (_type_): value = pandas dataframe
        """
        try:
            data = self.redis_get(redis_key)
            df_data = pickle.loads(zlib.decompress(data))
        except TypeError:
            print("value does not exist")
            df_data = pd.DataFrame()
        return df_data


if __name__ == "__main__":
    client = RedisClient(REDIS_UBUNTU_ADMIN)

    keys = client.redis_client.keys()
    print(keys)

    df1 = client.get_key_dataframe("DERIBIT_BTC_USD_INDEX")
    print(df1)
