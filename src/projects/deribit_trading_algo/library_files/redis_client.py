"""
https://redis.io/docs/clients/python/
pip install redis

redis is a NoSQL database
data is stored as key-value pairs

uses RAM to store data

to read on these methods
hgetall
bgsave
hset
hmset
"""
import pickle
import zlib

import pandas as pd
import redis

from local_credentials.db_credentials import AFTERSHOCK_PC_MICRO_REDIS


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

        Args:
            redis_key (str): key i.e BINANCE_BTC_USDT_ORDERBOOK
            redis_value (_type_): value = pandas dataframe
        """
        value = zlib.compress(pickle.dumps(redis_value))
        self.redis_client.set(name=redis_key, value=value)

    def get_key(self, redis_key: str):
        """gets value of specified redis_key
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
    client = RedisClient(AFTERSHOCK_PC_MICRO_REDIS)

    keys = client.redis_client.keys()
    print(keys)

    tables = client.redis_get_keys()
    print(tables)

    df1 = client.get_key("DERIBIT_BTC-PERPETUAL_ORDERBOOK")
    df2 = client.get_key("DERIBIT_ETH-PERPETUAL_ORDERBOOK")

    df3 = client.get_key("DERIBIT_BTC_POSITIONS")
    df4 = client.get_key("DERIBIT_ETH_POSITIONS")

    df5 = client.get_key("DERIBIT_BTC_USD_INDEX")
    df6 = client.get_key("DERIBIT_ETH_USD_INDEX")

    print(df1)
    print(df2)
    print(df3)
    print(df4)
    print(df5)
    print(df6)
