#!/bin/bash

source /home/edgar/github/python/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/github/python
echo "added $PYTHONPATH to python path"
echo $PYTHONPATH

python3 /home/edgar/github/python/src/crypto/execution_algo/bybit/bybit_virtual_account/spot_va.py
