# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 22:41:05 2023

@author: Tushar
"""
from alpha_vantage.timeseries import TimeSeries

api_key = 'YRW8N40DQYT9E11Y'
ts = TimeSeries(key=api_key)
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL')