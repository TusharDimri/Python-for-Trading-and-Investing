# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:13:50 2023

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

# Filling NaN Values:
# adj_close_prices.fillna(method='backfill', axis=0, inplace=True) # Value for axis: 0 is col and 1 is row

# Droppiong NaN Values 
adj_close_prices.dropna(axis=0, inplace=True) # Value for axis: 0 is col and 1 is row


