#!/bin/bash

source /home/edgar/github/python/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/github/python
echo "added $PYTHONPATH to python path"
echo $PYTHONPATH

python3 /home/edgar/github/python/src/crypto/execution_algo/binance/binance_spot_twap_limit/spot_twap_limit.py check