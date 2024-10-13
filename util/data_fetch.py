import json
import os

class Extractor():
    def __init__(self) -> None:
        self.files_path = {
                            'NSE':os.path.join('assets','nse_company_list.json'),
                            'INDEXNSE':os.path.join('assets','nse_indices_list.json'),
                            'INDEXBOM':os.path.join('assets','bse_indices_list.json'),
                            'NYSE':os.path.join('assets','nyse_company_list.json'),
                            'NASDAQ':os.path.join('assets','nasdaq_company_list.json'),
                            'GLOBAL_INDICES':os.path.join('assets','global_indices_list.json')
                       }
    def __find_symbol(self, ticker_symbol):
        for exchange_symbol,json_file in self.files_path.items():
            with open(os.path.join(os.getcwd(),json_file), 'r') as f:
                data = json.load(f)
                if ticker_symbol in data:
                    yield exchange_symbol
                else:
                    continue
    
    def get_data(self, ticker_symbol):
        exchange_symbol = self.__find_symbol(ticker_symbol=ticker_symbol)
        exchange_symbol = list(exchange_symbol)
        print("exchange_symbol",exchange_symbol)
        return exchange_symbol

if __name__ == "__main__":

    extractor = Extractor()
    print(extractor.get_data("NIFTY_50"))



