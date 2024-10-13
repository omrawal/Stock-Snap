from util.google_finance_extraction import StockQuoteFetcher
from util.data_fetch import Extractor


if __name__ == "__main__":
    ticker_symbol = input("Enter ticker Symbol").strip().upper()
    extractor = Extractor()
    exchange_symbols = extractor.get_data(ticker_symbol=ticker_symbol)
    for exchange_symbol in exchange_symbols:
        fetcher  = StockQuoteFetcher(company_symbol=ticker_symbol,exchange_symbol=exchange_symbol)
        print(fetcher.fetch_quote())
