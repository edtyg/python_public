#!/bin/bash

source /home/edgar/python/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/edgar/python/src
echo "added $PYTHONPATH to python path"

python3 /home/edgar/python/src/server_cronjobs/sgtrading1/portfolio_certificate_returns/main.py