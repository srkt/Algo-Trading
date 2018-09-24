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

        if self.source.upper() in "YAHOO,GOOGLE,STOOQ,MORNINGSTAR":

            if isinstance(ticker, str):
                try:
                    if str.upper(self.source) == 'STOOQ':
                        ticker = str.upper(ticker) + '.US'

                    return [(ticker, web.DataReader(ticker, self.source, from_date, end_date))]
                except:
                    print('error occurred while retreving stock data for : ' + ticker)

            elif isinstance(ticker, list):
                output = []

                for t in ticker:
                    if not isinstance(t, str):
                        raise Exception('invalid ticker passed')

                    try:
                        if str.upper(self.source) == 'STOOQ':
                            t = t.upper() + '.US'

                        output.append((t, web.DataReader(t, self.source, from_date, end_date)))
                    except:
                        print('error occurred while retreving stock data for : ' + t)

                return output

        elif self.source.upper() in 'QUANDL':

            output = []

            try:
                if isinstance(ticker, str):
                    return [(ticker, QuandlStockData().get_data(ticker, from_date, end_date))]

                if isinstance(ticker, list):
                    for t in ticker:
                        output.append((t, QuandlStockData().get_data(t, from_date, end_date)))
                    return output

            except:
                print('error occurred while retreving stock data for : ' + ticker)

        else:
            raise Exception('Currently only supports Yahoo, Google,Stooq and Quandl data sources')
