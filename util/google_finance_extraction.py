from bs4 import BeautifulSoup
import requests
import json

google_quote_base_url = "https://www.google.com/finance/quote/"
company_symbol = "ITC"
exchange_symbol = "NSE"
quote_lpt_class = "YMlKec fxKbKc"
description_class = "zzDege"

google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"

response = requests.get(google_quote_fetch_url)
soup = BeautifulSoup(response.text,"html.parser")
quote_ltp = ""
content =  soup.find(class_=quote_lpt_class)
if content is not None:
    quote_ltp = content.text
print(quote_ltp)

with open("symbols.json", "r") as symbols:
    company_symbol_list = json.load(symbols)


for company_symbol in company_symbol_list:
    google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"
    response = requests.get(google_quote_fetch_url)
    soup = BeautifulSoup(response.text, "html.parser")
    quote_ltp = ""
    desc = ""
    ltp_content = soup.find(class_=quote_lpt_class)
    desc_content = soup.find(class_=description_class)
    if ltp_content is not None:
        quote_ltp = ltp_content.text
    if desc_content is not None:
        desc = desc_content.text
    # print(quote_ltp)
    print({company_symbol : {'ltp':quote_ltp,'desc':desc}})