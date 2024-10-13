import json

class Extractor():
    def __init__(self) -> None:
        self.files_path = {
                            'NSE':'../assets/nse_company_list.json',
                            'INDEXNSE':'../assets/nse_indices_list.json',
                            'INDEXBOM':'../assets/bse_indices_list.json',
                            'NYSE':'../assets/nyse_company_list.json',
                            'NASDAQ':'../assets/nasdaq_company_list.json',
                            'GLOBAL_INDICES':'../assets/global_indices_list.json'
                       }
    def __find_symbol(self, ticker_symbol):
        for exchange_symbol,json_file in self.files_path.items():
            with open(json_file, 'r') as f:
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
    
extractor = Extractor()
print(extractor.get_data("NIFTY_50"))



