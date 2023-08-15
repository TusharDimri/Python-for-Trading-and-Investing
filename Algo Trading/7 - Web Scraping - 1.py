# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:40:02 2023

@author: Tushar
"""

import requests
from bs4 import BeautifulSoup

url = 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL'
headers = {"User-Agent":"Chrome/112.0.5615.138"}
page = requests.get(url, headers=headers)
page_content = page.content
income_statement={}

soup = BeautifulSoup(page_content, "html.parser")
table = soup.find_all("div", {"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})

for t in table:
    rows = t.find_all("div", {"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
    for row in rows:
        # print(row.get_text(separator="|"))
        income_statement[row.get_text(separator="|").split("|")[0]]= row.get_text(separator="|").split("|")[1]