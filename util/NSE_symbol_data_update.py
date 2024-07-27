from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# google_quote_base_url = "https://www.google.com/finance/quote/"
# company_symbol = "ITC"
# exchange_symbol = "NSE"
# quote_lpt_class = "YMlKec fxKbKc"
# description_class = "zzDege"

# with open("symbols.json", "r") as symbols:
#     company_symbol_list = json.load(symbols)

# for company_symbol in company_symbol_list:
#     if company_symbol_list[company_symbol] == "":
#         response = requests.get(google_quote_base_url+f"{company_symbol}:{exchange_symbol}")
#         soup = BeautifulSoup(response.text, "html.parser")
#         desc_content = soup.find(class_=description_class)
#         if desc_content is not None:
#             company_symbol_list[company_symbol] = desc_content.text
#             print(f"updated { company_symbol_list[company_symbol]}")

# with open("symbols_updated.json", "w+") as symbols_updated:
#     json.dump(company_symbol_list,symbols_updated)
# print("File created")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

# index_df = pd.read_csv("../assets/MW-All-Indices-27-Jul-2024.csv")
# print(index_df.columns)
# nse_indices_list = {}
# for i in range(len(index_df)):
#     symbol = index_df.loc[i]['INDEX \n'].replace(" ","_")
#     nse_indices_list[symbol] = ""

google_quote_base_url = "https://www.google.com/finance/quote/"
company_symbol = ""
exchange_symbol = "INDEXNSE"
description_class = "zzDege"

with open("nse_indices_list.json", "r") as symbols:
    nse_indices_list = json.load(symbols)
nse_indices_list_keys = nse_indices_list.keys()
nse_indices_list_updated = dict()
for company_symbol in nse_indices_list_keys:
    response = requests.get(google_quote_base_url + f"{company_symbol}:{exchange_symbol}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        desc_content = soup.find(class_=description_class)
        if desc_content is not None:
            print(company_symbol, response.status_code,desc_content.text)
            nse_indices_list_updated[company_symbol] = ""


with open("nse_indices_list_updated.json", "w+") as symbols_updated:
    json.dump(nse_indices_list_updated,symbols_updated)
print("File created")