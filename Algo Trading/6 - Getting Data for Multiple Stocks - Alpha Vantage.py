# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 22:50:12 2023

@author: Tushar
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

key_path = "D:\Python for Finance Investment Fundamentals & Data Analytics\Algo Trading"
#api_key = open(key_path, "r").read()

ts = TimeSeries(key="YRW8N40DQYT9E11Y", output_format="pandas")
# We get a tuple so we are usong the 0th index of that tuple
data=ts.get_intraday("AAPL", interval="60min", outputsize="full")[0] 
data.columns=["open", "high", "low", "close", "volume"]
data = data.iloc[::-1]

# Getting Data for multiple Tickers:

tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "GOOG", "FB"]
adj_close_prices = pd.DataFrame()
api_call_count = 0

for ticker in tickers:
    start_time = time.time()
    ts = TimeSeries(key="YRW8N40DQYT9E11Y", output_format="pandas")
    data=ts.get_intraday("AAPL", interval="60min", outputsize="full")[0]
    api_call_count += 1
    data.columns=["open", "high", "low", "close", "volume"]
    data = data.iloc[::-1]
    adj_close_prices[ticker] = data["close"]
    
    if api_call_count==4:
        api_call_count = 0
        time.sleep(60-(time.time()-start_time))
        

