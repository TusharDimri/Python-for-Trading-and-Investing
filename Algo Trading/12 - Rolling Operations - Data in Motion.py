# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:22:32 2023

@author: Tushar
"""


import datetime as dt
import yfinance as yf
import pandas as pd


stocks = ["AMZN", "MSFT", "META", "GOOG"]
start = dt.datetime.today() - dt.timedelta(4650)
end = dt.datetime.today()

adj_close_prices = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    adj_close_prices[ticker] = yf.download(ticker, start, end)["Adj Close"]


adj_close_prices.dropna(axis=0, inplace=True) 


daily_return = adj_close_prices.pct_change()
daily_return = adj_close_prices/adj_close_prices.shift(1)

daily_return_desc = daily_return.describe()

# This gives us 10 day moving average
rolling_mean = daily_return.rolling(window=10).mean()

# ewn is used for getting the Exponential Moving Average 
ema = daily_return.ewm(com=10, min_periods=10).mean()