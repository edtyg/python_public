"""
now defunct alameda trading
"""
import hmac
import time
from typing import Any, Dict, Optional

from requests import Request, Response, Session
from local_credentials.api_key_brokers import ALAMEDA_KEY, ALAMEDA_SECRET


class FtxOtcClient:
    """FTX OTC API"""

    _ENDPOINT = "https://otc.ftx.com/api/"

    def __init__(self, apikey: str, apisecret: str) -> None:
        self._session = Session()
        self._api_key = apikey
        self._api_secret = apisecret

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("POST", path, json=params)

    def _delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    def request_otc_quote(
        self,
        base_currency: str,
        quote_currency: str,
        side: str,
        base_currency_size: Optional[float] = None,
        quote_currency_size: Optional[float] = None,
        wait_for_price: bool = True,
    ) -> Any:
        """
        gets otc quotes
        """
        assert (quote_currency_size is None) ^ (base_currency_size is None)
        return self._post(
            "otc/quotes",
            {
                "baseCurrency": base_currency,
                "quoteCurrency": quote_currency,
                "baseCurrencySize": base_currency_size,
                "quoteCurrencySize": quote_currency_size,
                "waitForPrice": wait_for_price,
                "side": side,
            },
        )

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        self._sign_request(request, path)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request, path: str) -> None:
        timestamp = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f"{timestamp}{prepared.method}/{path}".encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(
            self._api_secret.encode(), signature_payload, "sha256"
        ).hexdigest()
        request.headers["FTX-APIKEY"] = self._api_key
        request.headers["FTX-TIMESTAMP"] = str(timestamp)
        request.headers["FTX-SIGNATURE"] = signature

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
            print(data)
        except ValueError:
            response.raise_for_status()
            raise

    def get_balances(self):
        """get balances"""
        return self._get("balances")


if __name__ == "__main__":
    client = FtxOtcClient(ALAMEDA_KEY, ALAMEDA_SECRET)
