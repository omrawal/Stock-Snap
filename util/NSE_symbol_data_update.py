from bs4 import BeautifulSoup
import requests
import json

google_quote_base_url = "https://www.google.com/finance/quote/"
company_symbol = "ITC"
exchange_symbol = "NSE"
quote_lpt_class = "YMlKec fxKbKc"
description_class = "zzDege"



with open("symbols.json", "r") as symbols:
    company_symbol_list = json.load(symbols)

for company_symbol in company_symbol_list:
    if company_symbol_list[company_symbol] == "":
        response = requests.get(google_quote_base_url+f"{company_symbol}:{exchange_symbol}")
        soup = BeautifulSoup(response.text, "html.parser")
        desc_content = soup.find(class_=description_class)
        if desc_content is not None:
            company_symbol_list[company_symbol] = desc_content.text
            print(f"updated { company_symbol_list[company_symbol]}")

with open("symbols_updated.json", "w+") as symbols_updated:
    json.dump(company_symbol_list,symbols_updated)
print("File created")