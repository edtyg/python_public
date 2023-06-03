"""
B2C2 API docs
https://docs.b2c2.net/
login is required to access the docs
"""
import requests
from local_credentials.api_key_brokers import B2C2_KEY


class B2C2Rest:
    """_summary_"""

    def __init__(self):
        self.base_endpoint = "https://api.b2c2.net"
        self.apikey = B2C2_KEY
        self.headers = {"Authorization": f"Token {self.apikey}"}
        self.timeout = 3

    def get_balances(self):
        """
        Get Balances
        https://docs.b2c2.net/#balances

        This shows the available balances in the supported currencies.
        Your account balance is the net result of all your trade and settlement activity.
        A positive number indicates that B2C2 owes you the amount of the given currency.
        A negative number means that you owe B2C2 the given amount.
        """

        endpoint = "/balance/"
        response = requests.request(
            "GET",
            self.base_endpoint + endpoint,
            headers=self.headers,
            timeout=self.timeout,
        )

        data = response.json()

        return data

    def get_tradable_instruments(self):
        """
        Get tradable instruments
        https://docs.b2c2.net/#get-tradable-instruments

        This endpoint returns the list of all the instruments you can trade.
        Please ask your sales representative if you want access to more instruments.
        """

        endpoint = "/instruments/"
        response = requests.request(
            "GET",
            self.base_endpoint + endpoint,
            headers=self.headers,
            timeout=self.timeout,
        )

        data = response.json()

        return data

    def get_currencies(self):
        """
        Get currencies
        https://docs.b2c2.net/#currencies

        Returns all currencies supported by B2C2 and the minimum trade sizes.
        Note that “long_only” means that your balance in this currency cannot be negative.
        """

        endpoint = "/currency/"
        response = requests.request(
            "GET",
            self.base_endpoint + endpoint,
            headers=self.headers,
            timeout=self.timeout,
        )

        data = response.json()

        return data

    def get_account_info(self):
        """
        Get account info
        https://docs.b2c2.net/#account-info

        Returns generic account information related to trading:
            current risk exposure,
            maximum risk exposure and maximum quantity allowed per trade.
            Note that the risk exposure can be computed by doing the
            sum of all of the negative balances in USD.
        """

        endpoint = "/account_info/"

        response = requests.request(
            "POST",
            self.base_endpoint + endpoint,
            headers=self.headers,
            timeout=self.timeout,
        )
        data = response.json()

        return data


if __name__ == "__main__":
    client = B2C2Rest()

    bal = client.get_balances()
    print(bal)
