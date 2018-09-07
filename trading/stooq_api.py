import pandas as pd

pd.core.common.is_list_like = pd.api.types.is_list_like
from trading.exchange import Exchange
import pandas_datareader.stooq as stooq
import pandas_datareader.data as web


class StooqExchange(Exchange):

    def __init__(self, source='stooq'):
        super(StooqExchange, self).__init__('Stooq Exchange')
        self.source = source

    def get_data(self, ticker, from_date='2018-01-01', end_date='2018-09-01'):
        data = web.DataReader(ticker, 'stooq', from_date, end_date)
        if not isinstance(data, pd.DataFrame):
            data = data.to_frame()

        return data
