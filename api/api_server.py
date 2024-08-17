# run using `uvicorn api_server:app --reload`

from fastapi import FastAPI
import os,sys
print(os.getcwd())
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.google_finance_extraction import StockQuoteFetcher
app = FastAPI()

@app.get("/")
def index():
    return {'message':"Welcome to Stock Price API"}

@app.get("/stock/{exchange_symbol}/{stock_symbol}")
def get_quote(exchange_symbol:str,stock_symbol:str):
    print("exchange_symbol",exchange_symbol,"stock_symbol",stock_symbol)
    fetcher = StockQuoteFetcher(stock_symbol.upper(),exchange_symbol.upper())
    quote_data = fetcher.fetch_quote()
    return {stock_symbol:quote_data}
