# https://docs.ftx.com/#overview
# last edited 30 Oct 2022

import time
import urllib.parse
from typing import Optional, Dict, Any, List
from requests import Request, Session, Response
import hmac

from crypto.platforms.ftx.rest.keys import *

class FtxClient:
    _ENDPOINT = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None, subaccount_name=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']
    
    ###################
    ### subaccounts ###
    ###################
    
    def get_all_subaccounts(self) -> List[dict]:
        # https://docs.ftx.com/#get-all-subaccounts
        return self._get('subaccounts')
    
    def create_subaccount(self, nickname: str) -> dict:
        # https://docs.ftx.com/#create-subaccount
        return self._post('subaccounts', {'nickname': nickname})
    
    def change_subaccount_name(self, nickname: str, new_nickname: str) -> None:
        # https://docs.ftx.com/#change-subaccount-name
        return self._post('subaccounts/update_name', {'nickname': nickname, 'newNickname': new_nickname})
    
    def delete_subaccount(self, nickname: str) -> None:
        # https://docs.ftx.com/#delete-subaccount
        return self._delete('subaccounts', {'nickname': nickname})
    
    def get_subaccount_balances(self, nickname: str) -> List[dict]:
        # https://docs.ftx.com/#get-subaccount-balances
        return self._get(f'subaccounts/{nickname}/balances')
    
    def transfer_between_subaccounts(self, coin: str, size: float, source: str, destination: str) -> dict:
        """_summary_

        Args:
            coin (str): BTC
            size (float): 0.1
            source (str): use 'main' for main account
            destination (str): use 'main' for main account

        Returns:
            dict
        """
        # https://docs.ftx.com/#transfer-between-subaccounts
        return self._post('subaccounts/transfer', {'coin': coin, 'size': size, 'source': source, 'destination': destination})
    
    ###############
    ### markets ###
    ###############
    
    def get_markets(self) -> List[dict]:
        # https://docs.ftx.com/#get-markets
        return self._get('markets')
    
    def get_single_market(self, market_name: str, depth: int = None) -> dict:
        # https://docs.ftx.com/#get-single-market
        return self._get(f'markets/{market_name}', {'depth': depth})
    
    def get_orderbook(self, market: str, depth: int = None) -> dict:
        # https://docs.ftx.com/#get-orderbook
        return self._get(f'markets/{market}/orderbook', {'depth': depth})
    
    def get_trades(self, market: str, start_time: float = None, end_time: float = None) -> List[dict]:
        # https://docs.ftx.com/#get-trades
        return self._get(f'markets/{market}/trades', {'start_time': start_time, 'end_time': end_time})
    
    def get_historical_prices(self, market: str, resolution: int = 300, start_time: float = None, end_time: float = None) -> List[dict]:
        # https://docs.ftx.com/#get-historical-prices
        return self._get(f'markets/{market}/candles', {'resolution': resolution, 'start_time': start_time, 'end_time': end_time})
    
    ###############
    ### futures ###
    ###############
    
    def list_all_futures(self) -> List[dict]:
        # https://docs.ftx.com/#list-all-futures
        return self._get('futures')

    def get_future(self, future_name: str = None) -> dict:
        # https://docs.ftx.com/#get-future
        return self._get(f'futures/{future_name}')

    def get_future_stats(self, future_name: str) -> dict:
        # https://docs.ftx.com/#get-future-stats
        return self._get(f'futures/{future_name}/stats')
    
    def get_funding_rates(self, future: str = None, start_time: float = None, end_time: float = None)-> List[dict]:
        # https://docs.ftx.com/#get-funding-rates
        return self._get('funding_rates', {'future': future, 'start_time': start_time, 'end_time': end_time})
    
    def get_index_weights(self, index_name: str)-> dict:
        """_summary_

        Args:
            index_name (str): ALT/MID/SHIT/EXCH/DRAGON

        Returns:
            dict
        """
        # https://docs.ftx.com/#get-index-weights
        return self._get(f'indexes/{index_name}/weights')
    
    def get_expired_futures(self) -> List[dict]:
        # https://docs.ftx.com/#get-expired-futures
        return self._get('expired_futures')
    
    def get_historical_index(self, market_name: str, resolution: int = 300, start_time: float = None, end_time: float = None) -> List[dict]:
        # https://docs.ftx.com/#get-historical-index
        return self._get(f'indexes/{market_name}/candles', {'resolution': resolution, 'start_time': start_time, 'end_time': end_time})
    
    def get_index_constituents(self, underlying: str) -> List[list]:
        # https://docs.ftx.com/#get-index-constituents
        return self._get(f'index_constituents/{underlying}')
    
    def get_funding_payments(self, future: str, start_time: float = None, end_time: float = None) -> List[list]:
        # https://docs.ftx.com/reference/get-funding-payments
        return self._get('funding_payments')
    
    ###############
    ### account ###
    ###############
    
    def get_account_infomation(self) -> dict:
        # https://docs.ftx.com/#get-account-information
        return self._get('account')
    
    def request_historical_balances_and_positions_snapshot(self, accounts: list, end_time: float) -> dict:
        # https://docs.ftx.com/#request-historical-balances-and-positions-snapshot
        return self._post('historical_balances/requests', {'accounts': accounts, 'endTime': end_time})
    
    def get_positions(self, show_avg_price: bool = False) -> List[dict]:
        # https://docs.ftx.com/reference/get-positions
        return self._get('positions', {'showAvgPrice': show_avg_price})
    
    def get_all_positions(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-all-positions
        return self._get('all_positions')
    
    def change_account_leverage(self, leverage: int) -> List[dict]:
        # https://docs.ftx.com/reference/change-account-leverage
        return self._post('account/leverage', {'leverage': leverage})
    
    def get_rate_limits(self) -> dict:
        # https://docs.ftx.com/reference/get-rate-limits
        return self._get('rate_limits')
    
    def get_api_keys(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-api-keys
        return self._get('api_keys')
    
    ##############
    ### wallet ###
    ##############
    
    def get_coins(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-coins
        return self._get('wallet/coins')
    
    def get_balances(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-balances
        return self._get('wallet/balances')
    
    def get_all_account_balances(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-all-account-balances
        return self._get('wallet/all_balances')
    
    def get_deposit_address(self, coin: str) -> dict:
        # https://docs.ftx.com/reference/get-deposit-address
        return self._get(f'wallet/deposit_address/{coin}')
    
    def get_deposit_address_list(self, coin: str, method: str = None) -> List[dict]:
        # https://docs.ftx.com/reference/get-deposit-address-list
        return self._post('wallet/deposit_address/list', {'coin': coin, 'method': method})
    
    def get_deposit_history(self, start_time: float = None, end_time: float = None) -> List[dict]:
        # https://docs.ftx.com/reference/get-deposit-history
        return self._get('wallet/deposits')
    
    def get_withdrawal_history(self, start_time: float = None, end_time: float = None) -> List[dict]:
        # https://docs.ftx.com/reference/get-withdrawal-history
        return self._get('wallet/withdrawals')
    
    ##############
    ### orders ###
    ##############
    
    def get_fills(self, market: str = None, start_time: float = None, end_time: float = None, min_id: int = None, order_id: int = None) -> List[dict]:
        # https://docs.ftx.com/reference/fills

        params = {
            'market': market,
            'start_time': start_time,
            'end_time': end_time,
            'minId': min_id,
            'orderId': order_id
            }
        return self._get('fills', params)
    
    def get_open_orders(self, market: str = None) -> List[dict]:
        # https://docs.ftx.com/reference/get-open-orders
        return self._get('orders', {'market': market})
    
    
    def place_order(self, market: str, side: str, price: float, size: float, type: str = 'limit', reduce_only: bool = False, 
                    ioc: bool = False, post_only: bool = False, client_id: str = None, reject_after_ts: float = None) -> dict:
        # https://docs.ftx.com/reference/place-order
        
        params = {
            'market': market,
            'side': side,
            'price': price,
            'size': size,
            'type': type,
            'reduceOnly': reduce_only,
            'ioc': ioc,
            'postOnly': post_only,
            'clientId': client_id,
            'rejectAfterTs': reject_after_ts,
            }
        return self._post('orders', params)
    
    def get_order_history(self, market: str = None, side: str = None, order_type: str = None, start_time: float = None, end_time: float = None) -> List[dict]:
        # https://docs.ftx.com/reference/get-order-history
        
        params = {
            'market': market,
            'side': side,
            'orderType': order_type,
            'start_time': start_time,
            'end_time': end_time
            }
        return self._get('orders/history', params)
    
    def get_order_status(self, order_id: str) -> List[dict]:
        # https://docs.ftx.com/reference/get-order-status
        return self._get(f'orders/{order_id}')
    
    def modify_order(self, existing_order_id: Optional[str] = None, price: Optional[float] = None, 
            size: Optional[float] = None, client_order_id: Optional[str] = None) -> dict:
        # https://docs.ftx.com/reference/modify-order
        return self._post(f'orders/{existing_order_id}/modify', {'size': size, 'price': price})
    
    def cancel_order(self, order_id: str) -> dict:
        # https://docs.ftx.com/reference/cancel-order
        return self._delete(f'orders/{order_id}')

    def cancel_all_orders(self, market_name: str = None, conditional_orders: bool = False, limit_orders: bool = False) -> dict:
        # https://docs.ftx.com/reference/cancel-all-orders
        
        body = {
            'market': market_name,
            'conditionalOrdersOnly': conditional_orders,
            'limitOrdersOnly': limit_orders
            }
        return self._delete('orders', body)
    
    ###################
    ### spot margin ###
    ###################
    
    def get_public_lending_history(self, start_time: float = None, end_time: float = None, coin: str = None) -> List[dict]:
        # https://docs.ftx.com/reference/get-lending-history
        return self._get('spot_margin/history')
    
    def get_borrow_rates(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-borrow-rates
        return self._get('spot_margin/borrow_rates')
    
    def get_lending_rates(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-lending-rates
        return self._get('spot_margin/lending_rates')
    
    def get_daily_borrowed_amounts(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-daily-borrowed-amounts
        return self._get('spot_margin/borrow_summary')
    
    def get_spot_margin_market_info(self, market: str) -> List[dict]:
        # https://docs.ftx.com/reference/get-spot-margin-market-info
        return self._get('spot_margin/market_info', {'market': market})
    
    def get_my_borrow_history(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-my-borrow-history
        return self._get('spot_margin/borrow_history')
    
    def get_my_lending_history(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-my-lending-history
        return self._get('spot_margin/lending_history')
    
    def get_lending_offers(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-lending-offers
        return self._get('spot_margin/offers')
    
    def get_lending_info(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-lending-info
        return self._get('spot_margin/lending_info')
    
    def submit_lending_offer(self, coin: str, size: float, rate: float) -> List[dict]:
        # https://docs.ftx.com/reference/submit-lending-offer
        params = {
            'coin': coin,
            'size': size,
            'rate': rate,
            }
        return self._post('spot_margin/offers', params)
    
    #############
    ### stats ###
    #############
    
    def get_latency_stats(self) -> List[dict]:
        # https://docs.ftx.com/reference/latency-statistics
        return self._get('stats/latency_stats')
    
    def get_24h_volume(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-24h-exchange-volume
        return self._get('stats/24h_volume')
    
    def get_30d_volume(self) -> List[dict]:
        # https://docs.ftx.com/reference/get-30d-exchange-volume
        return self._get('stats/30d_volume')
    
    def get_exchange_status(self) -> List[dict]:
        # https://docs.ftx.com/reference/exchange-status
        return self._get('busy')

if __name__ == "__main__":
    client = FtxClient(ed_api_key, ed_api_secret)