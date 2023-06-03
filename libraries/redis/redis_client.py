import redis
import pandas as pd
import pickle
import zlib


class RedisClient:
    def __init__(
        self,
        redis_host="192.168.1.122",
        redis_port=6379,
        redis_password=None,
        redis_db=0,
    ):
        pool = redis.ConnectionPool(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
        )

        self.redis_client = redis.Redis(connection_pool=pool)

    def save_df(self, df, df_name):
        self.redis_client.set(df_name, zlib.compress(pickle.dumps(df)))

    def get_df(self, df_name):
        try:
            data = self.redis_get(df_name)
            df = pickle.loads(zlib.decompress(data))

        except TypeError as err:
            print(
                f"redis_client.py: Tried to get df with key: {df_name}, got error: {err}"
            )
            df = pd.DataFrame()

        return df

    def redis_set(self, key, value):
        self.redis_client.set(key, value)

    def redis_get(self, key):
        return self.redis_client.get(key)

    def redis_get_keys(self):
        self.redis_client.keys()

    def redis_hgetall(self, id):
        return self.redis_client.hgetall(id)

    def redis_bgsave(self):
        self.redis_client.bgsave()


if __name__ == "__main__":
    redis_instance = RedisClient()

    keys = redis_instance.redis_client.keys()
    print(keys)

    # df1 = redis_instance.get_df('age')
    # print(df1)
