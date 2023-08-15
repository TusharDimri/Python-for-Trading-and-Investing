# -*- coding: utf-8 -*-
"""
Created on Wed May  3 22:43:13 2023

@author: Tushar
"""

import yfinance as yf
import numpy as np
import pandas as pd


tickers = ["GOOG", "AMZN", "MSFT"]
ohlcv_data = {}
sharpe_data = {}
sortino_data = {}

def CAGR(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252  # 252 is the number of trading days in an year
    CAGR = (df["cumulative_return"][-1])**(1/n) - 1
    return CAGR

def VOLATILITY(DF):
    df = DF.copy()
    df["returns"] = df["Adj Close"].pct_change()
    daily_volatility = df["returns"].std()
    annual_volatility = np.sqrt(252) * daily_volatility
    return annual_volatility


def SHARPE_RATIO(DF, risk_free_rate=0.03):
    df = DF.copy()
    sharpe = (CAGR(df) - risk_free_rate)/VOLATILITY(df)
    return sharpe

def SORTINO_RATIO(DF, risk_free_rate=0.03):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    negative_returns = np.where(df["return"]>0, 0, df["return"])
    negative_volatility = pd.Series((negative_returns!=0)).std()
    sortino = (CAGR(df) - risk_free_rate)/negative_volatility
    return sortino
    
for ticker in tickers:
    temp = yf.download(ticker, period='7mo', interval='1d')
    temp.dropna(how='any', inplace=True)
    ohlcv_data[ticker] = temp
    sharpe_data[ticker] = SHARPE_RATIO(ohlcv_data[ticker])
    sortino_data[ticker] = SORTINO_RATIO(ohlcv_data[ticker])