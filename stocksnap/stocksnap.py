from .util.google_finance_extraction import StockQuoteFetcher
import json

class StockSnap(object):
    """
    StockSnap Class
    This class is used to fetch real-time stock market data for a given ticker symbol across different exchanges.
    """
    def __init__(self) -> None:
        self.exchange_symbols = ['NSE',
                            'INDEXNSE',
                            'INDEXBOM',
                            'NYSE',
                            'NASDAQ']

    def fetch_details(self,ticker_symbol) -> dict:
        """
        Fetches the stock quote details for a given ticker symbol.
        
        Args:
            ticker_symbol (str): The ticker symbol of the company/index.

        Returns:
            dict: A dictionary with exchange symbols as keys and their corresponding stock quote details as values.
        """
        response = {}
        for exchange_symbol in self.exchange_symbols:
            fetcher  = StockQuoteFetcher(company_symbol=ticker_symbol.upper(),exchange_symbol=exchange_symbol)
            quote_response = json.loads(fetcher.fetch_quote())
            if len(quote_response['ltp']) != 0:
                response[exchange_symbol] = quote_response

        return json.dumps(response)