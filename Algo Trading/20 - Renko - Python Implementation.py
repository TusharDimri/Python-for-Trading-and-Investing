# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 18:18:41 2023

@author: Tushar
"""

import yfinance as yf
from stocktrends import Renko

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}
hour_data = {}
renko_data = {}

# For deciding the Brick Size we'll be using ATR on hourly data:
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

def RENKO_DF(DF, hourly_df):
    df = DF.copy()
    # First we'll drop unwanted(wrt stocktrends) Columns:
    df.drop("Close", axis=1, inplace=True)
    df.reset_index(inplace=True)
    # Changing column names as per the syntax of Renko(from stocktrends):
    df.columns = ["date", "open", "high", "low", "close", "volume"]
    
    df2 = Renko(df)
    df2.brick_size = 3 * round(ATR(hourly_df, 120).iloc[-1], 1)
    renko_df = df2.get_ohlc_data()
    return renko_df
    
    

for ticker in tickers:
    temp = yf.download(ticker, period="1mo", interval='5m')
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    
    temp = yf.download(ticker, period="1y", interval='1h')
    temp.dropna(how="any", inplace=True)
    hour_data[ticker] = temp
    renko_data[ticker] = RENKO_DF(ohlcv_data[ticker], hour_data[ticker])