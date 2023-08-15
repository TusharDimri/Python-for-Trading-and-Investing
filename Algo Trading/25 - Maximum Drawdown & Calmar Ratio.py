# -*- coding: utf-8 -*-
"""
Created on Wed May  3 23:07:43 2023

@author: Tushar
"""


import yfinance as yf
import matplotlib

tickers = ["GOOG", "AMZN", "MSFT"]
ohlcv_data = {}
cagr = {}
max_drawdown = {}
calmar_ratio = {}


def MAX_DRAWDOWN(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["Compounded Return"] = (1+df["return"]).cumprod()
    df["Compounded Return"].plot()
    df["Cumulative_Rolling_Max"] = df["Compounded Return"].cummax()
    df["Drawdown"] = df["Cumulative_Rolling_Max"] - df["Compounded Return"] 
    max_drawdown =  (df["Drawdown"]/df["Cumulative_Rolling_Max"]).max() 
    return max_drawdown
    
def CAGR(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252  # 252 is the number of trading days in an year
    CAGR = (df["cumulative_return"][-1])**(1/n) - 1
    return CAGR

def CALMAR_RATIO(cagr, max_drawdown):
    return cagr/max_drawdown

for ticker in tickers:
    temp = yf.download(ticker, period='7mo', interval='1d')
    temp.dropna(how='any', inplace=True)
    ohlcv_data[ticker] = temp
    cagr[ticker] = CAGR(ohlcv_data[ticker])
    max_drawdown[ticker] = MAX_DRAWDOWN(ohlcv_data[ticker]) * 100
    calmar_ratio[ticker] = CALMAR_RATIO(cagr[ticker], max_drawdown[ticker])