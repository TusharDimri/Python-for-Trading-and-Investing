# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 11:25:06 2023

@author: Tushar
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

def ATR(DF, n=14):
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = df["High"] - df["Adj Close"].shift(1)
    df["L-PC"] = df["Low"] - df["Adj Close"].shift(1)
    df["True Range"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    # df["ATR"] = df["True Range"].ewm(span=n, min_periods=n).mean()
    df["ATR"] = df["True Range"].ewm(com=n, min_periods=n).mean() 
    # We used com here cause we get closer to Yahoo Finance calucation of EMA if we use com
    return df["ATR"]
    
for ticker in tickers:
    temp = yf.download(ticker, period="1mo", interval='5m')
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    ohlcv_data[ticker]["ATR"] = ATR(ohlcv_data[ticker])