import requests
from bs4 import BeautifulSoup
import json


class StockQuoteFetcher:
    """ 
    A class to fetch stock quotes from Google Finance.
    """
    CURRENCY_SYMBOLS = {"$": "USD", "₹": "INR"}

    def __init__(self, company_symbol, exchange_symbol):
        self.google_quote_base_url = "https://www.google.com/finance/quote/"
        self.company_symbol = company_symbol
        self.exchange_symbol = exchange_symbol
        self.quote_lpt_class = "YMlKec fxKbKc"
        self.description_class = "zzDege"
        self.prev_close_class = "gyFHrc"
        self.long_desc_class = "bLLb2d"
        self.ltp = ""
        self.description = ""
        self.long_desc = ""
        self.currency = ""
        self.currency_symbol = ""
        self.previous_close = ""
        self.percentage_change = 0.0
        self.change_amount = 0.0
        self.change_type = "UP"

    def fetch_soup(self):
        """ 
        Fetch the HTML content of the Google Finance page for the stock. 
        
        Returns: 
        BeautifulSoup object of the fetched HTML content. 
        """
        url = f"{self.google_quote_base_url}{self.company_symbol}:{self.exchange_symbol}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_currency_and_symbol(self, value_string):
        """ Extract the currency and its symbol from the value string. 
        
        Parameters: 
        value_string : str : The string containing the currency symbol and value. 
        
        Returns: 
        tuple : A tuple containing the currency name and symbol. 
        """
        currency_symbol = value_string[0]
        if currency_symbol in self.CURRENCY_SYMBOLS:
            return self.CURRENCY_SYMBOLS[currency_symbol], currency_symbol
        return None, None

    def get_ltp_string(self, soup):
        """ 
        Extract the latest trading price (LTP) from the soup. 
        
        Parameters: 
        soup : BeautifulSoup : The parsed HTML content. 
        
        Returns: 
        str : The latest trading price as a string. 
        """
        ltp_content = soup.find(class_=self.quote_lpt_class)
        if ltp_content is not None:
            return ltp_content.text.replace(",", "")
        # print("LTP content is None")
        return None

    def get_previous_close_string(self, soup):
        """ 
        Extract the previous closing price from the soup. 
        
        Parameters: 
        soup : BeautifulSoup : The parsed HTML content. 
        
        Returns: 
        str : The previous closing price as a string. 
        """
        previous_close_content = soup.find_all(class_=self.prev_close_class)
        if previous_close_content:
            previous_close_tag = BeautifulSoup(str(previous_close_content[0]), "html.parser")
            previous_close_value = previous_close_tag.find(class_="P6K39c").text.replace(",", "")
            return previous_close_value
        # print("Previous close content is None")
        return None

    def get_long_description_string(self, soup):
        """
        Extract the long description of the company from the soup.

        Parameters:
        soup : BeautifulSoup : The parsed HTML content.

        Returns:
        str : The description of the company as a string.
        """
        long_desc_content = soup.find(class_=self.long_desc_class)
        if long_desc_content is not None:
            return long_desc_content.text
        # print("Long description content is None")
        return None

    def get_amount_change_and_percentage_change(self):
        """ 
        Calculate the amount change and percentage change in stock price. 
        """
        self.change_amount = float(self.ltp) - float(self.previous_close)
        self.percentage_change = (abs(self.change_amount) * 100) / float(self.previous_close)
        self.change_type = "DOWN" if self.change_amount < 0 else "UP"

    def fetch_quote(self):
        """ 
        Fetch the stock quote and related information. 
        
        Returns: 
        str : JSON string containing the stock information. 
        """
        soup = self.fetch_soup()
        ltp_str_value = self.get_ltp_string(soup)
        if ltp_str_value:
            self.ltp = ltp_str_value
            self.currency, self.currency_symbol = self.get_currency_and_symbol(ltp_str_value)
            if self.currency:
                self.ltp = ltp_str_value[1:]

        else:
            # print("LTP string value is None",ltp_str_value)
            pass

        long_desc_string = self.get_long_description_string(soup)
        if long_desc_string:
            self.long_desc = long_desc_string

        prev_close_str_value = self.get_previous_close_string(soup)
        if prev_close_str_value:
            self.previous_close = prev_close_str_value
            prev_close_currency, prev_close_currency_symbol = self.get_currency_and_symbol(prev_close_str_value)
            if prev_close_currency:
                self.previous_close = prev_close_str_value[1:]

        if self.ltp and self.previous_close:
            self.get_amount_change_and_percentage_change()

        desc_content = soup.find(class_=self.description_class)
        if desc_content is not None:
            self.description = desc_content.text

        return json.dumps({
            'ticker_symbol': self.company_symbol,
            'exchange_symbol': self.exchange_symbol,
            'ltp': self.ltp,
            'desc': self.description,
            "long_desc" : self.long_desc,
            "previous_close": self.previous_close,
            "currency": self.currency,
            "percentage_change": f"{self.percentage_change}%",
            "change_amount": self.change_amount,
            "currency_symbol": self.currency_symbol,
            "change_type": self.change_type
        })


def get_quote(ticker_symbol, exchange_ticker_symbol):
    """ 
    Get the stock quote for a given ticker symbol and exchange symbol.
    
    Parameters: 
    ticker_symbol : str : The stock ticker symbol. 
    exchange_ticker_symbol : str : The stock exchange symbol. 
    
    Returns: dict : Dictionary containing the stock quote data. 
    """
    try:
        fetcher = StockQuoteFetcher(ticker_symbol, exchange_ticker_symbol)
        quote_data = fetcher.fetch_quote()
        return {ticker_symbol: quote_data}
    except Exception as e:
        return {"Some error occurred in fetching quote: ": e}


if __name__ == "__main__":
    # get_all_quotes(json_file_path="../assets/nse_indices_list.json", exchange_symbol="INDEXNSE")
    # get_all_quotes(json_file_path="../assets/bse_indices_list.json", exchange_symbol="INDEXBOM")
    # get_all_quotes(json_file_path="../assets/nse_company_list.json", exchange_symbol="NSE")
    # get_all_quotes(json_file_path="../assets/nyse_company_list.json", exchange_symbol="NYSE")
    # get_all_quotes(json_file_path="../assets/nasdaq_company_list.json", exchange_symbol="NASDAQ")

    print(get_quote("HDFCBANK", "NSE"))
    print(get_quote("HDB", "NYSE"))
    print(get_quote("GOOGL", "NASDAQ"))
    print(get_quote("SENSEX", "INDEXBOM"))
    print(get_quote("NIFTY_50", "INDEXNSE"))
