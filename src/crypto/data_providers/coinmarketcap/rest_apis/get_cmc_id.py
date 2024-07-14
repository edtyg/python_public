"""
Get coinmarketcap ids
"""

import pandas as pd

from crypto.data_providers.coinmarketcap.rest_apis.user import cmc_user

if __name__ == "__main__":
    cmc_id = cmc_user.get_cmc_id_map()

    data = cmc_id["data"]
    df_data = pd.DataFrame(data)
    df_data = df_data.loc[df_data["symbol"] == "WLD"]
    print(df_data)

    # top 30 by marketcap
    # df_data_mcap_sorted = df_data.sort_values(by="rank").head(30)
    # print(df_data_mcap_sorted)
