# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 20:22:45 2023

@author: Tushar
"""
import numpy as np
import talib
import copy
from alpha_vantage.timeseries import TimeSeries

tickers = ["MSFT", "AAPL", "META", "AMZN", "CSCO", "VZ", "IBM", "QCOM", "LYFT"]
api_key = 'YRW8N40DQYT9E11Y'
ts = TimeSeries(key=api_key, output_format="pandas")

# OHLC Value for each tech stack:
ohlc_tech = {}

# initializing passthorough variable
attempt = 0

# initializing list to store tickers whose close price was successfully extracted:
drop = []

while len(tickers)!=0 and attempt<=100:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            ohlc_tech[tickers[i]] =  ts.get_intraday(symbol=tickers[i], outputsize="full")[0]
            ohlc_tech[tickers[i]].columns = ["Open", "High", "Low", "Adj Close", "Volume"]
            drop.append(tickers[i])
        except:
            print(tickers[i], "Failed to load data... retrying")
            continue
    attempt+=1
        
# redifine ticker variable after removing any tickers with corrupted data: 
tickers = ohlc_tech.keys()
ohlc_dict = copy.deepcopy(ohlc_tech)

for ticker in tickers:
    ohlc_dict[ticker]["3 Inisde"] = talib.CDL3INSIDE(ohlc_dict[ticker]["Open"],
                                                     ohlc_dict[ticker]["High"],
                                                     ohlc_dict[ticker]["Low"], 
                                                     ohlc_dict[ticker]["Adj Close"])
    