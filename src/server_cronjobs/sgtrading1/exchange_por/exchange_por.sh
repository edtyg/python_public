#!/bin/bash

source /home/edgar/venv/trading/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar
echo "added $PYTHONPATH to python path"

python3 /home/edgar/python/sg1_server/cronjobs/exchange_por/wallet_balances.py