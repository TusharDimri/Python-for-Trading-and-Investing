# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:45:55 2023

@author: Tushar
"""


import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib

stocks = ["AMZN", "MSFT", "META", "GOOG"]
start = dt.datetime.today() - dt.timedelta(4650)
end = dt.datetime.today()

adj_close_prices = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    adj_close_prices[ticker] = yf.download(ticker, start, end)["Adj Close"]


adj_close_prices.dropna(axis=0, inplace=True) 

daily_return = adj_close_prices.pct_change()
# daily_return = adj_close_prices/adj_close_prices.shift(1)

adj_close_prices.plot(subplots=True, layout=(2, 2), title='Stock Price Evolution', grid=True)
daily_return.plot(subplots=True, layout=(2, 2), title='Daily Returns', grid=True)

# cumprod() function - Cumulative Product - gives us the compounded returns
compounded_return = (1 + daily_return).cumprod()
compounded_return.plot(subplots=True, layout=(2, 2), title='Compounded Returns', grid=True)