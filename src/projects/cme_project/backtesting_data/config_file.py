"""
Config file for backtesting

using CME CF BRRAP - Bitcoin reference rate Asia Pacific time: 3-4pm HKT
using Binance and OKX trade records during 3-4pm HKT
"""

# Partition k - split up into K partitions for trades
k = 3600

# Weights - Weightage given to Exchanges - make sure to sum = 1
weight = {
    "Binance": 0.6,
    "Okx": 0.4,
}
