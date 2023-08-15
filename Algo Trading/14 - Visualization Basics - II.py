# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 22:30:56 2023

@author: Tushar
"""


import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN", "MSFT", "META", "GOOG"]
start = dt.datetime.today() - dt.timedelta(4650)
end = dt.datetime.today()

adj_close_prices = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    adj_close_prices[ticker] = yf.download(ticker, start, end)["Adj Close"]


adj_close_prices.dropna(axis=0, inplace=True) 

daily_return = adj_close_prices.pct_change()

fig, ax = plt.subplots()
ax.set(title = "Mean Daily Returns", xlabel="Stocks", ylabel="Mean Return")
# print(plt.style.available)
plt.style.use("ggplot")
#plt.bar(x=daily_return.columns, height=daily_return.mean(), color = ['red', 'blue', 'green', 'orange'])
plt.bar(x=daily_return.columns, height=daily_return.mean())
# plt.bar(x=daily_return.columns, height=daily_return.std())