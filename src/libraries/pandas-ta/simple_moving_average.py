"""
pip install pandas_ta
pip install mplfinance
"""

import mplfinance as mpf
import pandas_ta as ta
import yfinance as yf

# Download historical stock data
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-01"
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Calculate simple moving averages
stock_data["sma_20"] = ta.sma(stock_data["Close"], length=20)
stock_data["sma_50"] = ta.sma(stock_data["Close"], length=50)

# Prepare the data for mplfinance
stock_data.index.name = "Date"  # Ensure the index is named 'Date'
mpf_data = stock_data[["Open", "High", "Low", "Close", "Volume"]]

# Define the moving averages to be plotted
add_plot = [
    mpf.make_addplot(stock_data["sma_20"], color="maroon", label="20-day SMA"),
    mpf.make_addplot(stock_data["sma_50"], color="blue", label="50-day SMA"),
]

my_style = mpf.make_mpf_style(
    # base_mpf_style="blueskies",
    marketcolors=mpf.make_marketcolors(
        up="green",
        down="red",
        edge="inherit",
        wick="inherit",
        volume="inherit",
    ),
    # figcolor="navy",
    # facecolor="black",
    edgecolor="black",
    gridcolor="grey",
    # gridstyle="--",
)
# Plotting the candlestick chart
mpf.plot(
    mpf_data,
    type="candle",
    style=my_style,  # style here
    addplot=add_plot,
    title="AAPL Stock Price with Moving Averages",
    ylabel="Price",
    volume=True,  # Include volume in the plot
    figsize=(16, 9),
    # mav=(20, 50),  # Add moving averages
    # tight_layout=True,
    # returnfig=True,  # Return the figure and axes for further customization
)
