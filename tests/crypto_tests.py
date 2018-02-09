import matplotlib.pyplot as plt
import util.keys as util
import technical.indicators as ind
import technical.screener as sc
import pandas as pd
import datetime as dt

from trading.binance_exchange import Binance
from trading.stock_exchange import StockExchange


def get_stockdata(ticker='sq'):
    path = "C:\Users\suman\Desktop\\" + ticker + ".csv"
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.now()

    se = StockExchange()
    data = se.get_data(ticker, start, end)
    save_data(data, path)
    return data


def save_data(df, path):
    if not isinstance(df, pd.DataFrame) or len(path) == 0:
        raise Exception('Pandas DataFrame expected')

    if len(path) == 0:
        raise Exception('Invalid path')

    df.to_csv(path)


def get_data_from_csv(path, ticker):
    fp = path + ticker + ".csv"

    print(fp)

    data = pd.DataFrame.from_csv(fp)

    return data


def get_data():
    key, secret = util.ks()
    coin_pair = 'BTCETH'
    path = "C:\Users\suman\Desktop\\" + coin_pair + ".csv"
    sample = Binance(key, secret)
    # df = sample.get_klines(Client.KLINE_INTERVAL_1DAY, 'BTC', 'ADA')
    df = sample.get_data(coin_pair, dt.datetime(2017, 11, 1), dt.datetime.now())

    save_data(df, path)
    print(df.info())
    return df


def test_macd(df):
    macd, signal = ind.Macd(df, 'close', 12, 21, 9)

    plt.plot(macd)
    plt.plot(signal)
    plt.legend(['macd', 'signal'])
    plt.show()


def test_rsi(df):
    rsi = ind.get_rsi(df, 14, 'close')

    plt.plot(rsi)
    plt.axhline(50, color='r', linestyle='--')
    plt.axhline(80, color='b', linestyle=':')
    plt.axhline(20, color='b', linestyle=':')

    plt.legend(['rsi'])
    plt.show()


def RunScreener(df):
    close_column = 'Close'
    volume_column = 'Volume'
    # Stratagies
    emrev = sc.EmaReversion(df, close_column, 12, 21)
    bb = sc.Bollinger(df, close_column, 14)
    sco = sc.StochasticOscillator(df, 14, name=close_column)
    mcd = sc.Macd(df, close_column)
    vwap = sc.Vwap(df, close_column, vol_col_name=volume_column)
    rsi = sc.Rsi(df, name=close_column)

    # create screener
    screener = sc.Screener(df)

    # add to screener
    screener.add_strategy(emrev)
    screener.add_strategy(bb)
    screener.add_strategy(sco)
    screener.add_strategy(rsi)
    screener.add_strategy(mcd)
    screener.add_strategy(vwap)

    results = screener.run()

    for result in results:
        print('Strategy : ' + result.strategy_name + ', signal : ' + result.buy_sell + ', weight: ' + str(
            result.weight))

    print('Current price:' + str(df[close_column][-1]))

    plt.figure(figsize=(16, 10))
    x = plt.subplot2grid((9, 1), (0, 0), rowspan=5)
    x.plot(df[close_column])
    x.plot(emrev.min_sma, 'r--')
    x.plot(emrev.max_sma, 'b--')
    x.plot(bb.output[['mean']], 'g-.')
    x.plot(bb.output[['up_std']], 'r.')
    x.plot(bb.output[['low_std']], 'r.')

    x.legend(['close', 'min sma', 'max sma', 'mean', 'up_std', 'low_std'])

    y = plt.subplot2grid((9, 1), (5, 0), rowspan=2)
    y.plot(sco.K)
    y.plot(sco.D)
    y.legend(['K', 'D'])

    zz = plt.subplot2grid((9, 1), (7, 0), rowspan=2)
    zz.plot(mcd.macd)
    zz.plot(mcd.signal)
    zz.legend(['MACD', 'Signal'])

    plt.show()


data = get_stockdata('SPY')
RunScreener(data)