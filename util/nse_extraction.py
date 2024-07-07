import requests
from bs4 import BeautifulSoup

nse_equity_url = "https://www.nseindia.com/get-quotes/equity?symbol="
symbol = "RELIANCE"

url = nse_equity_url + symbol
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
print("before extraction")
with requests.session() as s:

    response = s.get(url=url,headers=headers)
    response = s.get(url=url,headers=headers)

    # print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)
print("After extraction")
