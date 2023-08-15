# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:47:08 2023

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

mean =  adj_close_prices.mean()
standard_deviation = adj_close_prices.std()
median = adj_close_prices.median()
desc = adj_close_prices.describe()

"All Quantitative Finance Methods focus on Asset Returns and not the Asset Price"

daily_return = adj_close_prices.pct_change()
daily_return = adj_close_prices/adj_close_prices.shift(1)

daily_return_desc = daily_return.describe()