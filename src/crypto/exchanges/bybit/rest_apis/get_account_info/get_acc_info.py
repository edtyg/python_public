"""
Bybit Account info - check if it's UTA
"""

from crypto.exchanges.bybit.rest_apis.accounts import BYBIT_MCA_LTP1_TRADE

if __name__ == "__main__":
    account = BYBIT_MCA_LTP1_TRADE

    # account_info = account.get_account_info()
    # print(account_info)

    # account_collateral_info = account.get_collateral_info()
    # print(account_collateral_info)

    # account_positions = account.get_position_info(
    #     {
    #         "category": "spot",
    #         "symbol": "BTCUSDT",
    #     }
    # )
    # print(account_positions)
