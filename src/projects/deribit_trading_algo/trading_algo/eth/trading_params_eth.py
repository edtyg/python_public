"""
trading parameters
"""
# import datetime as dt

##########################
### trading parameters ###
### short strangles ######
CONTRACT_SIZE = 1  # orders have to be in multiples of 1 USD
BASE_CAPITAL = 5  # starting ETH amount - not needed in algo
POSITIONAL_SIZE = 25  # rough positions you should have on - 5x

SHORT_PUT_STRIKE = 1750
SHORT_CALL_STRIKE = 1850
STRIKE_INTERVAL = 50  # +- 50 from strike price
DELTA_THRESHOLD = 1  # current vs expected delta > then threshold. place order
