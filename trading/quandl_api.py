from trading.exchange import Exchange
import pandas as pd
import quandl


class QuandlStockData(Exchange):
    API_KEY = 'rwcM5he_sxH2VoscWvsT'  # '4HyLLeq1LKXyUxZdL61p' #
    quandl.ApiConfig.api_key = API_KEY

    def __init__(self, source='quandl'):
        super(QuandlStockData, self).__init__('Stock Exchange')
        self.source = source

    def get_data(self, ticker, from_date='2018-01-01', end_date='2018-09-01'):
        data = quandl.get_table('WIKI/PRICES', ticker=[ticker],
                                qopts={'columns': ['ticker', 'date', 'close', 'volume']},
                                date={'gte': from_date, 'lte': end_date})

        return data
