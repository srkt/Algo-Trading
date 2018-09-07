import pandas as pd

from trading.quandl_api import QuandlStockData

pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime as dt
from trading.exchange import Exchange


class StockExchange(Exchange):

    def __init__(self, source='google'):
        super(StockExchange, self).__init__('Stock Exchange')
        self.source = source

    def get_data(self, ticker, from_date, end_date):
        if not isinstance(from_date, dt.datetime) and not isinstance(end_date, dt.datetime):
            raise Exception('Expected datetime format of datetime.datetime')

        if self.source.upper() in "YAHOO,GOOGLE,STOOQ":
            if isinstance(ticker, str):
                try:
                    return [(ticker, web.DataReader(ticker, self.source, from_date, end_date))]
                except:
                    print('error occurred while retreving stock data for : ' + ticker)
            elif isinstance(ticker, list):
                output = []
                for t in ticker:
                    if not isinstance(t, str):
                        raise Exception('invalid ticker passed')
                    try:
                        output.append((t, web.DataReader(t, self.source, from_date, end_date)))
                    except:
                        print('error occurred while retreving stock data for : ' + t)

            return output
        else:
            raise Exception('invalid ticker passed. Expected either string or list')

        if self.source.upper() in 'QUANDL':
            try:
                data = QuandlStockData().get_data(ticker, from_date, end_date)
            except:
                print('error occurred while retreving stock data for : ' + ticker)
