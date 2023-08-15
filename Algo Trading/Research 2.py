# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 00:42:33 2023

@author: Tushar
"""

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

ticker = '^NSEI'

data = yf.download(ticker, start='2021-09-04', end='2023-06-04', interval='1h')
data.reset_index(inplace=True)

data['MovingAverage'] = data['Adj Close'].rolling(window=50).mean()

X = np.arange(len(data)).reshape(-1, 1)
y = data['Adj Close'].values.reshape(-1, 1)
regression = LinearRegression().fit(X, y)
regression_line = regression.predict(X)

# Calculate standard deviation
std_dev = np.std(y - regression_line)

# Calculate upper and lower bounds
upper_bound = regression_line + 2 * std_dev
lower_bound = regression_line - 2 * std_dev

# Plot the data, regression line, and bounds
plt.figure(figsize=(12, 6))
plt.plot(data['Datetime'], data['Adj Close'], label='Stock Price')
plt.plot(data['Datetime'], data['MovingAverage'], label='Moving Average (50)')
plt.plot(data['Datetime'], regression_line, label='Regression Line')
plt.plot(data['Datetime'], upper_bound, 'r--', label='Upper Bound')
plt.plot(data['Datetime'], lower_bound, 'r--', label='Lower Bound')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Linear Regression with 50-Period Moving Average')
plt.legend()
plt.grid(True)
plt.show()
