# -*- coding: utf-8 -*-
"""
Created on Mon May  1 23:19:27 2023

@author: Tushar
"""

import yfinance as yf

tickers = ["GOOG", "AMZN", "MSFT"]
ohlcv_data = {}
cagr_dict = {}

def CAGR(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252  # 252 is the number of trading days in an year
    # If the data was hourly: 
    # n = (len(df)/6)/252 
    CAGR = (df["cumulative_return"][-1])**(1/n) - 1
    return CAGR
    
for ticker in tickers:
    temp = yf.download(ticker, period='7mo', interval='1d')
    temp.dropna(how='any', inplace=True)
    ohlcv_data[ticker] = temp
    cagr_dict[ticker] = CAGR(ohlcv_data[ticker])
    