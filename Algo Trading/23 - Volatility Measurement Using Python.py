# -*- coding: utf-8 -*-
"""
Created on Tue May  2 23:57:48 2023

@author: Tushar
"""

import yfinance as yf
import numpy as np

tickers = ["GOOG", "AMZN", "MSFT"]
ohlcv_data = {}
volatility_dict = {}

def VOLATILITY(DF):
    df = DF.copy()
    df["returns"] = df["Adj Close"].pct_change()
    daily_volatility = df["returns"].std()
    annual_volatility = np.sqrt(252) * daily_volatility
    return annual_volatility

for ticker in tickers:
    temp = yf.download(ticker, period='7mo', interval='1d')
    temp.dropna(how='any', inplace=True)
    ohlcv_data[ticker] = temp
    volatility_dict[ticker] = round(VOLATILITY(ohlcv_data[ticker]), 2)
    