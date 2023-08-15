# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 23:15:53 2023

@author: Tushar
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["ema_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
    df["ema_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
    df["MACD"] = df["ema_fast"] - df["ema_slow"]
    df["SIGNAL"] = df["MACD"].ewm(span=c, min_periods=c).mean()
    return df.loc[:, ["MACD", "SIGNAL"]]

for ticker in tickers:
    temp = yf.download(ticker, period="1mo", interval='15m')
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    ohlcv_data[ticker][["MACD", "SIGNAL"]] = MACD(ohlcv_data[ticker])
    
    