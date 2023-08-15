# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 11:47:21 2023

@author: Tushar
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

def BOLLINGER_BAND(DF, n=14):
    df = DF.copy()
    df["Middle Band"] = df["Adj Close"].rolling(n).mean()
    df["Upper Band"] = df["Middle Band"] + 2 * df["Adj Close"].rolling(n).std(ddof=0)
    df["Lower Band"] = df["Middle Band"] - 2 * df["Adj Close"].rolling(n).std(ddof=0)
    df["Band Width"] = df["Upper Band"] - df["Lower Band"]
    return df[["Middle Band", "Upper Band", "Lower Band", "Band Width"]]

for ticker in tickers:
    temp = yf.download(ticker, period="1mo", interval='5m')
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    ohlcv_data[ticker][["Middle Band", "Upper Band", "Lower Band", "Band Width"]] = BOLLINGER_BAND(ohlcv_data[ticker], 20)