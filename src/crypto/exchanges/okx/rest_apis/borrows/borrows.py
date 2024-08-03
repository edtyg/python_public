"""
SPOT execution program
"""

from keys.api_work.crypto_exchanges.okx import OKX_KEYS
from src.crypto.exchanges.okx.rest.okx_client import Okx

if __name__ == "__main__":
    account = OKX_KEYS["OKX_MCA_LTP1_READ"]
    okx_client = Okx(
        apikey=account["api_key"],
        apisecret=account["api_secret"],
        passphrase=account["passphrase"],
    )

    # borrow_limit = okx_client.get_borrow_interest_limit(
    #     {
    #         "type": 2,
    #         "ccy": "BTC",
    #     }
    # )
    # print(borrow_limit)

    fixed_borrow_limit = okx_client.get_fixed_loan_borrow_limit()
    print(fixed_borrow_limit)
