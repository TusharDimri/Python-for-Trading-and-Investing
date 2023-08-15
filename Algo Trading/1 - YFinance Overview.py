# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:51:43 2023

@author: Tushar
"""

import yfinance as yf

# data = yf.download('MSFT', period='6mo')
data = yf.download('MSFT', start='2022-02-28', end='2023-04-15', interval='1h')
