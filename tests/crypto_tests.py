import matplotlib.pyplot as plt
import util.keys as util
import technical.indicators as ind
import technical.screener as sc
import pandas as pd
import datetime as dt

from trading.binance_exchange import Binance
from trading.stock_exchange import StockExchange


def get_stockdata(ticker='sq'):
    start = dt.datetime(2017, 7, 1)
    end = dt.datetime.now()
    se = StockExchange()
    data = se.get_data(ticker, start, end)
    return data


def save_data(df, path):
    if not isinstance(df, pd.DataFrame) or len(path) == 0:
        raise Exception('Pandas DataFrame expected')

    if len(path) == 0:
        raise Exception('Invalid path')

    df.to_csv(path)


def get_data_from_csv(path, ticker):
    fp = path + ticker + ".csv"

    data = pd.DataFrame.from_csv(fp)

    return data

def get_exc_info():
    key, secret = util.ks()
    sample = Binance(key, secret)
    info = sample.getExchangeInfo()
    print(info)

def get_ticker_info():
    key, secret = util.ks()
    sample = Binance(key, secret)
    info = sample.get_all_tickers()
    print(info.head(100))

def get_data():
    key, secret = util.ks()
    coin_pair = 'BTCETH'
    path = "C:\Users\suman\Desktop\\" + coin_pair + ".csv"
    sample = Binance(key, secret)
    # df = sample.get_klines(Client.KLINE_INTERVAL_1DAY, 'BTC', 'ADA')
    df = sample.get_data(coin_pair, dt.datetime(2017, 11, 1), dt.datetime.now())

    save_data(df, path)
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


def RunScreener(df, ticker_name):
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

    fig = plt.figure(figsize=(16, 16))
    plt.title(ticker_name)
    x = plt.subplot2grid((12, 1), (0, 0), rowspan=6, title=ticker_name)
    x.plot(df[close_column])
    x.plot(emrev.min_sma, 'r--')
    x.plot(emrev.max_sma, 'b--')
    x.plot(bb.output[['mean']], 'm-')
    x.plot(bb.output[['up_std']], 'r:')
    x.plot(bb.output[['low_std']], 'g:')

    x.legend(['close', 'min sma', 'max sma', 'mean', 'up_std', 'low_std'])

    y = plt.subplot2grid((12, 1), (6, 0), rowspan=2)
    y.plot(sco.K)
    y.plot(sco.D)
    y.legend(['K', 'D'])

    z = plt.subplot2grid((12, 1), (8, 0), rowspan=2)
    z.plot(rsi.rsi)
    z.axhline(y=80, color='r', linestyle='--')
    z.axhline(y=50, color='b', linestyle='--')
    z.axhline(y=20, color='g', linestyle='--')

    z.legend(['RSI'])

    zz = plt.subplot2grid((12, 1), (10, 0), rowspan=2)
    zz.plot(mcd.macd)
    zz.plot(mcd.signal)
    zz.axhline(y=0, color='r', linestyle=':')
    zz.legend(['MACD', 'Signal'])

    return fig

get_ticker_info()

# tickers = ['SPY', 'SQ', 'TWTR', 'SNAP']
# tickers = ['ABEV']
# data = get_stockdata(tickers)
# for sdata in data:
#     path = "C:\Users\suman\Desktop\Stocks\{}.csv".format(sdata[0])
#     save_data(sdata[1], path)
#     fig = RunScreener(sdata[1], sdata[0])
#     img = "C:\Users\suman\Desktop\Stocks\{}.png".format(sdata[0])
#     fig.savefig(img)
