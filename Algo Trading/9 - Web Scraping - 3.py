# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:32:23 2023

@author: Tushar
"""
from bs4 import BeautifulSoup
import requests

tickers = ["AAPL", "CSCO", "INFY.NS", "3988.HK"]
headers = {"User-Agent":"Chrome/112.0.5615.138"}
key_statistics = {}

for ticker in tickers:
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p=AAPL"
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")

    tabl = soup.find_all("table", {"class":"W(100%) Bdcl(c)"})

    temp_stats = {}
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            temp_stats[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[-1]
    
    key_statistics[ticker] = temp_stats