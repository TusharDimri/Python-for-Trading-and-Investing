# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:52:12 2023

@author: Tushar
"""
import datetime as dt
from yahoofinancials import YahooFinancials

ticker = 'MSFT'
yahoo_financials = YahooFinancials(ticker)
data = yahoo_financials.get_historical_price_data("2022-04-24", "2023-04-24", "daily")
