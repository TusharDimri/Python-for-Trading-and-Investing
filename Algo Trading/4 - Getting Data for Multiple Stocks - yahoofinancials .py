# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 22:07:21 2023

@author: Tushar
"""

import datetime as dt
import pandas as pd
from yahoofinancials import YahooFinancials

stocks = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]

adj_close_prices = pd.DataFrame()

end_date = (dt.date.today()).strftime("%Y-%m-%d")
start_date = (dt.date.today()-dt.timedelta(1825)).strftime("%Y-%m-%d")

for ticker in stocks:
    yahoo_financials = YahooFinancials(ticker)
    json_data = yahoo_financials.get_historical_price_data(start_date, end_date, "daily")  
    ohlcv = json_data[ticker]["prices"]
    temp = pd.DataFrame(ohlcv)[["formatted_date", "adjclose"]]
    temp.set_index("formatted_date", inplace=True)
    temp.dropna(inplace=True)
    adj_close_prices[ticker] = temp["adjclose"]