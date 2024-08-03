"""
Utility Class
"""

from typing import Dict, Optional

import requests
from requests.exceptions import HTTPError, RequestException, Timeout


class Utils:
    """
    this class serves as a utility class, that provides commonly used functions
    """

    @staticmethod
    def get_request(
        base_url: str,
        endpoint: Optional[str] = None,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ):
        """Rest requests with error handling
        GET Requests only, timeout set to 5 seconds

        ["GET", "POST", "DELETE", "PUT"] -> some common request methods

        Args:
            base_url (str): base endpoint
            endpoint (Optional[str]): endpoint of your api call
            params (Optional[Dict]): params for your api call if required
        """
        try:
            response = requests.request(
                method="GET",
                url=base_url + endpoint,
                headers=headers,
                params=params,
                timeout=5,
            )
            return response.json()

        except HTTPError as http_error:
            # 404 or 500 error
            print(f"HTTP Error: {http_error}")

        except Timeout as timeout_error:
            # Request timed out
            print(f"Request Timed out: {timeout_error}")

        except RequestException as request_error:
            # Other requests error
            print(f"Request error: {request_error}")

        except ValueError as json_error:
            # Json decoding error
            print(f"JSON decode error: {json_error}")

        except Exception as error:
            # other exceptions
            print(f"An unexpected error occurred: {error}")
