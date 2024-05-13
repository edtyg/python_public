"""
pip install yfinance
"""

# https://pypi.org/project/yfinance/

import yfinance as yf

msft = yf.Ticker("MSFT")

info = msft.info  # get stock info
hist = msft.history(period="max")  # get historical market data
action = msft.actions  # show actions (dividends, splits)
dividends = msft.dividends  # show dividends
splits = msft.splits  # show splits
fin = msft.financials  # show financials
qtr_fin = msft.quarterly_financials  # qtrly financials
maj_hol = msft.major_holders  # show major holders
insti = msft.institutional_holders  # show institutional holders
bs = msft.balance_sheet  # balance sheet
qty_bs = msft.quarterly_balance_sheet  # qtrly balance sheet
cf = msft.cashflow  # show cashflow
qty_cf = msft.quarterly_cashflow  # qtrly cashflow
earn = msft.earnings  # show earnings
qty_earn = msft.quarterly_earnings  # qtrly earnings
sus = msft.sustainability  # show sustainability
rec = msft.recommendations  # show analysts recommendations
cal = msft.calendar  # show next event (earnings, etc)
earn = msft.earnings_dates  # show all earnings dates
ii = msft.isin  # ISIN = International Securities Identification Number
news = msft.news  # show news
opt = msft.options  # show options expirations

d = "2022-12-02"
opt_chain = msft.option_chain(d)  # option chain - specified date


data = yf.download("SPY", start="2022-01-01", end="2022-12-31")
data = yf.download(
    # tickers list or string as well
    tickers="SPY AAPL MSFT",
    # use "period" instead of start/end
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # (optional, default is '1mo')
    period="ytd",
    # fetch data by interval (including intraday if period < 60 days)
    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # (optional, default is '1d')
    interval="1m",
    # Whether to ignore timezone when aligning ticker data from
    # different timezones. Default is True. False may be useful for
    # minute/hourly data.
    ignore_tz=False,
    # group by ticker (to access via data['SPY'])
    # (optional, default is 'column')
    group_by="ticker",
    # adjust all OHLC automatically
    # (optional, default is False)
    auto_adjust=True,
    # download pre/post regular market hours data
    # (optional, default is False)
    prepost=True,
    # use threads for mass downloading? (True/False/Integer)
    # (optional, default is True)
    threads=True,
    # proxy URL scheme use use when downloading?
    # (optional, default is None)
    proxy=None,
)
