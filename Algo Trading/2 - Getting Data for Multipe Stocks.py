# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:05:36 2023

@author: Tushar
"""

import yfinance as yf
import datetime as dt
import pandas as pd

stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS", "3988.HK"]
start = dt.datetime.today() - dt.timedelta(days=360)
end = dt.datetime.today()
adj_close_df = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    adj_close_df[ticker] = yf.download(ticker, start, end)["Adj Close"]    

for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start, end)    
    