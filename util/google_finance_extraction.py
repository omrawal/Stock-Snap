from bs4 import BeautifulSoup
import requests

google_quote_base_url = "https://www.google.com/finance/quote/"
company_symbol = "ITC"
exchange_symbol = "NSE"
quote_lpt_class = "YMlKec fxKbKc"

google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"

response = requests.get(google_quote_fetch_url)
soup = BeautifulSoup(response.text,"html.parser")
quote_ltp = soup.find(class_=quote_lpt_class).text
print(quote_ltp)