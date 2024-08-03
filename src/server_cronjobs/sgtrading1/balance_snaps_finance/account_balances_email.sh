#!/bin/bash

source /home/edgar/python/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/python/src:/home/edgar/python
echo "added $PYTHONPATH to python path"

python3 /home/edgar/python/src/server_cronjobs/sgtrading1/balance_snaps_finance/account_balances_email.py
