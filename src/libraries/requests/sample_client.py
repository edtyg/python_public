""" sample request method"""

import requests


def _get(endpoint: str):
    """
    Standard Get Request
    """
    response = requests.get(endpoint, timeout=5)

    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    test_endpoint = "https://blockchain.info/q/getblockcount"

    data = _get(test_endpoint)
    print(data)
