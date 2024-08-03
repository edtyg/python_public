#!/bin/bash

source /home/edgar/python/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/python
echo "added $PYTHONPATH to python path"
echo $PYTHONPATH

python3 /home/edgar/python/src/server_cronjobs/sgtrading2/postgres_database/save_klines/bybit/upload_bybit_data.py ethusdt