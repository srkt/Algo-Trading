from binance.client import Client
import pandas as pd
from tzlocal import get_localzone
import datetime as dt
from trading.exchange import Exchange


class Binance(Exchange):
    close_column_name = 'close'
    volume_colume_name = 'volume'

    # @staticmethod
    # @property
    # def close_column_name():
    #     return 'close'

    def get_data(self, ticker, from_date, end_date, interval=Client.KLINE_INTERVAL_1HOUR):

        if len(ticker) == 0:
            raise Exception('ticker is invalid')

        if isinstance(ticker, str):
            base_coin = ticker[:3]
            alt_coin = ticker[3:]
            return self.get_klines(base_coin=base_coin, alt_coin=alt_coin, start_date=from_date, end_date=end_date)

        if isinstance(ticker, list):
            result = []
            for t in ticker:
                base_coin = t[:3]
                alt_coin = t[3:]
                result.append(
                    (t, self.get_klines(base_coin=base_coin, alt_coin=alt_coin, start_date=from_date, end_date=end_date)
                     ))
            return result

    @staticmethod
    def get_date_string(date_time):

        if not isinstance(date_time, dt.datetime):
            raise Exception('Datetime expected')

        return date_time.strftime('%d %b, %Y')

    def __init__(self, key, secret):
        super(Binance, self).__init__('Binance')

    kline_columns = ['openTime',
                     'open',
                     'high',
                     'low',
                     'close',
                     'volume',
                     'closeTime',
                     'quoteAssetVolume',
                     'trades',
                     'takerBaseAssetVolume',
                     'takerQuoteAssetVolume', 'ignored']

    baseCoin = 'BTC'
    altCoin = ''
    coin_pair = baseCoin + altCoin

    def getExchangeInfo(self):
        client = Client(self.key, self.secret)
        return client.get_exchange_info()

    def get_all_tickers(self):
        client = Client(self.key, self.secret)
        tickers = client.get_all_tickers()
        return pd.DataFrame(tickers)

    def __init__(self, key, secret, base_coin="BTC", alt_coin="XRP"):
        super(Binance, self).__init__('Binance')
        self.key = key
        self.secret = secret
        self.set_coin_pair(base_coin, alt_coin)

    def set_coin_pair(self, base_coin, alt_coin):
        self.altCoin = alt_coin
        self.baseCoin = base_coin
        self.coin_pair = alt_coin + base_coin

    def get_klines(self, period=Client.KLINE_INTERVAL_1HOUR,
                   base_coin='BTC',
                   alt_coin='XRP',
                   localize_time=True,
                   index_time_column_name='closeTime',
                   start_date=None,
                   end_date=None):

        self.set_coin_pair(base_coin, alt_coin)
        client = Client(self.key, self.secret)

        if start_date is None and end_date is None:
            candles = client.get_klines(symbol=self.coin_pair, interval=period)
        else:
            start_str = Binance.get_date_string(start_date)
            end_str = Binance.get_date_string(end_date)
            candles = client.get_historical_klines(symbol=self.coin_pair, interval=period,
                                                   start_str=start_str, end_str=end_str)

        df = pd.DataFrame(candles)
        df.columns = self.kline_columns

        df['open'] = pd.to_numeric(df['open'])
        df['close'] = pd.to_numeric(df['close'])
        df['volume'] = pd.to_numeric(df['volume'])

        if localize_time:
            mytz = get_localzone()
            df['openTime'] = pd.to_datetime(df['openTime'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(mytz)
            df['closeTime'] = pd.to_datetime(df['closeTime'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(mytz)

        if index_time_column_name == 'closeTime':
            df.set_index('closeTime', inplace=True)

        if index_time_column_name == 'openTime':
            df.set_index('openTime', inplace=True)

        return df
