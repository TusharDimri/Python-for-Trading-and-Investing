# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:40:31 2023

@author: Tushar
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL", "CSCO", "INFY.NS", "3988.HK"]
headers = {"User-Agent":"Chrome/112.0.5615.138"}

income_statement_dict = {}
balance_sheet_dict = {}
cash_flow_statement_dict = {}

for ticker in tickers:
    # Scraping Income Statement:
    income_statement = {}
    table_title = {}
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    tabl = soup.find_all("div", {"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div", {"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    temp = pd.DataFrame(income_statement).T        
    temp.columns = table_title["Breakdown"]
    income_statement_dict[ticker] = temp
    
    # Scraping Balance Sheet:
    balance_sheet = {}
    table_title = {}
    url = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}"
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    tabl = soup.find_all("div", {"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div", {"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            balance_sheet[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    temp = pd.DataFrame(balance_sheet).T        
    temp.columns = table_title["Breakdown"]
    balance_sheet_dict[ticker] = temp
    
    # Scraping Cash Flow Statement:
    cash_flow_statement = {}
    table_title = {}
    url = f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}"
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    tabl = soup.find_all("div", {"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all("div", {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div", {"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            cash_flow_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    temp = pd.DataFrame(cash_flow_statement).T        
    temp.columns = table_title["Breakdown"]
    cash_flow_statement_dict[ticker] = temp
    
# Converting Data into Numeric Data:
for ticker in tickers:
     for col in income_statement_dict[ticker].columns:
         income_statement_dict[ticker][col] = income_statement_dict[ticker][col].str.replace(",|-", "")
         income_statement_dict[ticker][col] = pd.to_numeric(income_statement_dict[ticker][col], errors="coerce")
         
     for col in balance_sheet_dict[ticker].columns:
         balance_sheet_dict[ticker][col] = balance_sheet_dict[ticker][col].str.replace(",|-", "")
         balance_sheet_dict[ticker][col] = pd.to_numeric(balance_sheet_dict[ticker][col], errors="coerce")
         
     for col in cash_flow_statement_dict[ticker].columns:
         cash_flow_statement_dict[ticker][col] = cash_flow_statement_dict[ticker][col].str.replace(",|-", "")
         cash_flow_statement_dict[ticker][col] = pd.to_numeric(cash_flow_statement_dict[ticker][col], errors="coerce")
    