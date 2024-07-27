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
content =  soup.find(class_=quote_lpt_class)
if content is not None:
    quote_ltp = content.text
print(quote_ltp)


def get_quotes_of_all_500_nse_companies():

    with open("../assets/nse_500_companies_symbols.json", "r") as symbols:
        company_symbol_list = json.load(symbols)

    for company_symbol in company_symbol_list:
        print("checking for company_symbol:", company_symbol)
        google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"
        response = requests.get(google_quote_fetch_url)
        soup = BeautifulSoup(response.text, "html.parser")
        quote_ltp = ""
        desc = ""
        currency = ""
        currency_symbol = ""
        percentage_change = ""
        change_amount = ""
        change_type = "UP" # UP / DOWN

        ltp_content = soup.find(class_=quote_lpt_class)
        desc_content = soup.find(class_=description_class)
        percentage_change_content = soup.find_all(class_=percentage_change_class)[27]
        if ltp_content is not None:
            quote_ltp = ltp_content.text.replace(",", "")
            currency_symbol = quote_ltp[0]

            if currency_symbol in CURRENCY_SYMBOLS:
                currency = CURRENCY_SYMBOLS[currency_symbol]
                quote_ltp = quote_ltp[1:]
            else:
                currency = "Unknown"

            percentage_change = percentage_change_content.text[:-1].replace(",","")
            if percentage_change[0] == "-":
                percentage_change = percentage_change[1:]
                change_type = "DOWN"

            change_amount = round(float(quote_ltp) * float(percentage_change) / 100, 2)

        if desc_content is not None:
            desc = desc_content.text

        # print("change_amount", change_amount)
        # print(quote_ltp)
        print({company_symbol: {'ltp': quote_ltp, 'desc': desc,
                                "currency": currency,"percentage_change": percentage_change+str("%"),
                                "change_amount": change_amount, "currency_symbol": currency_symbol,
                                "change_type": change_type}})

get_quotes_of_all_500_nse_companies()