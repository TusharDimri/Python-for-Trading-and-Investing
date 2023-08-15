# -*- coding: utf-8 -*-
"""
Created on Sat May 13 10:32:47 2023

@author: Tushar
"""

import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

tickers = ["MMM","AXP","T","BA","CAT","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UNH","VZ","V","WMT","DIS"]

ohlcv_data = {}
cagr = {}
max_drawdown = {}
calmar_ratio = {}
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()


def CAGR(DF):
    df = DF.copy()
    # df["returns"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = (1 + df["monthly_returns"]).cumprod()
    # n = len(df)/252  # 252 is the number of trading days in an year
    n = len(df)/12  # 12 is the number of months in an year
    CAGR = (df["cumulative_return"][-1])**(1/n) - 1
    return CAGR

def VOLATILITY(DF):
    df = DF.copy()
    # df["returns"] = df["Adj Close"].pct_change()
    daily_volatility = df["monthly_returns"].std()
    # annual_volatility = np.sqrt(252) * daily_volatility
    annual_volatility = np.sqrt(12) * daily_volatility
    return annual_volatility



def SHARPE_RATIO(DF, risk_free_rate=0.03):
    df = DF.copy()
    sharpe = (CAGR(df) - risk_free_rate)/VOLATILITY(df)
    return sharpe

def SORTINO_RATIO(DF, risk_free_rate=0.03):
    df = DF.copy()
    # df["returns"] = df["Adj Close"].pct_change()
    negative_returns = np.where(df["monthly_returns"]>0, 0, df["monthly_returns"])
    negative_volatility = pd.Series((negative_returns!=0)).std()
    sortino = (CAGR(df) - risk_free_rate)/negative_volatility
    return sortino

def MAX_DRAWDOWN(DF):
    df = DF.copy()
    # df["return"] = df["Adj Close"].pct_change()
    df["Compounded Return"] = (1+df["monthly_returns"]).cumprod()
    df["Compounded Return"].plot()
    df["Cumulative_Rolling_Max"] = df["Compounded Return"].cummax()
    df["Drawdown"] = df["Cumulative_Rolling_Max"] - df["Compounded Return"] 
    max_drawdown =  (df["Drawdown"]/df["Cumulative_Rolling_Max"]).max() 
    return max_drawdown
    

def CALMAR_RATIO(cagr, max_drawdown):
    return cagr/max_drawdown

for ticker in tickers:
    temp = yf.download(ticker,start,end,interval='1mo')
    temp.dropna(how='any', inplace=True)
    ohlcv_data[ticker] = temp
    
tickers = ohlcv_data.keys()

ohlcv_dict = copy.deepcopy(ohlcv_data)
returns_df = pd.DataFrame()

for ticker in tickers:
    print(f"Calculating Monthly Returns of: {ticker}")
    ohlcv_dict[ticker]["monthly_returns"] = ohlcv_dict[ticker]["Adj Close"].pct_change()
    returns_df[ticker] = ohlcv_dict[ticker]["monthly_returns"]
returns_df.dropna(inplace=True)