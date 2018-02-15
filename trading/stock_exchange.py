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

        if isinstance(ticker, str):
            return [(ticker, web.DataReader(ticker, self.source, from_date, end_date))]
        elif isinstance(ticker, list):
            output = []
            for t in ticker:
                if not isinstance(t, str):
                    raise Exception('invalid ticker passed')
                output.append((t, web.DataReader(t, self.source, from_date, end_date)))

            return output
        else:
            raise Exception('invalid ticker passed. Expected either string or list')
