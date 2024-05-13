"""
trading parameters
"""
# import datetime as dt

##########################
### trading parameters ###
### short strangles ######
CONTRACT_SIZE = 10  # orders have to be in multiples of 10 USD
BASE_CAPITAL = 0.4  # starting ETH amount - not needed in algo
POSITIONAL_SIZE = 2  # rough positions you should have on - 5x

SHORT_PUT_STRIKE = 26500
SHORT_CALL_STRIKE = 27000
STRIKE_INTERVAL = 250  # +- 50 from strike price
DELTA_THRESHOLD = 0.1  # current vs expected delta > then threshold. place order
