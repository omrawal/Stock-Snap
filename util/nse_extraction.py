from bs4 import BeautifulSoup
import requests
import json

google_quote_base_url = "https://www.google.com/finance/quote/"
company_symbol = "ITC"
exchange_symbol = "NSE"
quote_lpt_class = "YMlKec fxKbKc"
description_class = "zzDege"
percentage_change_class = "JwB6zf"
CURRENCY_SYMBOLS = {"$": "USD", "₹": "INR"}

google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"

response = requests.get(google_quote_fetch_url)
soup = BeautifulSoup(response.text,"html.parser")
quote_ltp = ""
ltp_content = soup.find(class_=quote_lpt_class)
if ltp_content is not None:
    quote_ltp = ltp_content.text
print("quote_ltp", quote_ltp)
currency = ""
currency_symbol = quote_ltp[0]
if currency_symbol in CURRENCY_SYMBOLS:
    currency = CURRENCY_SYMBOLS[currency_symbol]
    quote_ltp = quote_ltp[1:]
else:
    currency = "Unknown"

percentage_change = soup.find_all(class_=percentage_change_class)[27].text
print("percentage_change",percentage_change)
amount_change = round(float(quote_ltp) * float(percentage_change[:-1])/100, 2)
print("amount_change",amount_change)






