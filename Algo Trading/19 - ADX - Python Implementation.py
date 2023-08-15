# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 13:18:56 2023

@author: Tushar
"""


import yfinance as yf
import numpy as np

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

def ADX(DF, n=20):
    df = DF.copy()
    #  For ADX calculation we'll need ATR:
    df["ATR"] = ATR(df, n)
    
    df["Up Move"] = df["High"] - df["High"].shift(1)
    df["Down Move"] = df["Low"].shift(1) - df["Low"]
    
    df["+dm"] = np.where((df["Up Move"] > df["Down Move"]) & (df["Up Move"] > 0), df["Up Move"], 0)
    df["-dm"] = np.where((df["Down Move"] > df["Up Move"]) & (df["Down Move"] > 0), df["Down Move"], 0)
    
    df["+di"] = 100 * (df["+dm"] / df["ATR"]).ewm(com=n, min_periods=n).mean()
    df["-di"] = 100 * (df["-dm"] / df["ATR"]).ewm(com=n, min_periods=n).mean()
    
    df["ADX"] = 100 * abs((df["+di"] - df["-di"])/(df["+di"]+df["-di"])).ewm(com=n, min_periods=n).mean() 
    
    return df["ADX"]
    
    
for ticker in tickers:
    temp = yf.download(ticker, period="1mo", interval='5m')
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    ohlcv_data[ticker]["ADX"] = ADX(ohlcv_data[ticker])