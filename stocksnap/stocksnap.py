from .util.google_finance_extraction import StockQuoteFetcher
from .util.symbol_fetch import Extractor

class StockSnap(object):
    """
    StockSnap Class
    This class is used to fetch real-time stock market data for a given ticker symbol across different exchanges.
    """
    def __init__(self) -> None:
        self.extractor = Extractor()

    def fetch_details(self,ticker_symbol) -> dict:
        """
        Fetches the stock quote details for a given ticker symbol.
        
        Args:
            ticker_symbol (str): The ticker symbol of the company/index.

        Returns:
            dict: A dictionary with exchange symbols as keys and their corresponding stock quote details as values.
        """
        response = {}
        exchange_symbols = self.extractor.get_data(ticker_symbol=ticker_symbol.upper())
        for exchange_symbol in exchange_symbols:
            fetcher  = StockQuoteFetcher(company_symbol=ticker_symbol.upper(),exchange_symbol=exchange_symbol)
            response [exchange_symbol] = fetcher.fetch_quote()
        return response