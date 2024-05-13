#!/bin/bash

source /home/edgar/venv/trading/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/github
echo "added $PYTHONPATH to python path"
echo $PYTHONPATH

python3 /home/edgar/github/python/projects/postgres_database/upload_binance_data.py
