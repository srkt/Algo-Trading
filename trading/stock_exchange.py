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

        return web.DataReader(ticker, self.source, from_date, end_date)
