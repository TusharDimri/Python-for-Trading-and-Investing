# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 12:27:37 2023

@author: Tushar
"""

import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

def RSI(DF, n):
    df = DF.copy()
    df["change"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["gain"] = np.where(df["change"]>=0, df["change"], 0)
    df["loss"] = np.where(df["change"]<0, df["change"] * -1, 0)
    df["Avg Gain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean()
    df["Avg Loss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
    df["Relative Strength"] = df["Avg Gain"] / df["Avg Loss"]
    df["RSI"] = 100 - (100 / (1 + df["Relative Strength"]))
    return df[["RSI"]]    
    
for ticker in tickers:
    temp = yf.download(ticker, period="1mo", interval='5m')
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    ohlcv_data[ticker]["RSI"] = RSI(ohlcv_data[ticker], 14)