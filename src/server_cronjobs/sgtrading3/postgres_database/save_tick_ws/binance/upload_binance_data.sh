#!/bin/bash

source /home/edgar/python/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/python
echo "added $PYTHONPATH to python path"
echo $PYTHONPATH

python3 /home/edgar/python/src/server_cronjobs/sgtrading3/postgres_database/save_tick_ws/binance/upload_binance_data.py