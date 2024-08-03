# Deribit trading algo - set up on ubuntu

## library_files
1) deribit_rest_client.py \
    rest methods for deribit api \

2) deribit_methods.py \
    built on deribit's rest api \
    maker orders etc... \
    
3) keys.py \
    api keys here \

4) redis_client.py \
    for interacting with local redis server \
    
5) slack_program.py \
    for posting messages in slack \

## orderbook_data
1) btc \
    deribit_websocket_orderbook_btc_perp.py \
        saving btc top of orderbook data into redis \
        
2) eth \
    deribit_websocket_orderbook_eth_perp.py \
        saving eth top of orderbook data into redis \
    
## positions_data
1) btc \
    deribit_websocket_btc_positions.py \
        saving btc positions and greeks into redis \
        
2) eth \
    deribit_websocket_eth_positions.py \
        saving eth positions and greeks into redis \

## index_prices
1) btc \
    deribit_websocket_btc_index.py \
        saving btc index price redis \
        
2) eth \
    deribit_websocket_eth_index.py \
        saving eth index price into redis \

## slack_messager
1) btc \
    slack_btc_positions_messager.py \
        sending messages to slack \
    
2) eth \
    slack_eth_positions_messager.py \
        sending messages to slack \

## trading_algo
1) btc \
    deribit_btc_trading_algo_taker.py \ 
    deribit_btc_trading_algo_maker.py \
        
2) eth \
    deribit_eth_trading_algo_taker.py \
    deribit_eth_trading_algo_maker.py \

## ubuntu_setup
1) setup.txt








