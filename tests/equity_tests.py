import matplotlib.pyplot as plt
import technical.indicators as ind
import technical.screener as sc
import pandas as pd
import datetime as dt
from trading.pandas_data_reader_api import StockExchange
from trading.quandl_api import QuandlStockData
from trading.stooq_api import StooqExchange


def get_stockdata(ticker='sq'):
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.now()
    se = StockExchange(source='stooq')  # QuandlStockData()
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

    print('Current price:' + str(df[close_column].iloc[-1]))

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


# get_ticker_info()

ticker = ['COG.US',
          'CY.US'
          'VOD.US',
          'HST.US',
          'INFY.US',
          'EXEL.US',
          'MRVL.US',
          'ABEV.US',
          'CRON.US',
          'CTL.US',
          'IPG.US',
          'STM.US',
          'ON.US',
          'HBI.US',
          'VIPS.US',
          'ARNC.US',
          'ETE.US',
          'SLCA.US']

ticker = ['ETE.US', 'SLCA.US']
listofstockdata = get_stockdata(ticker)
for stockinfo in listofstockdata:
    ticker = stockinfo[0]
    stockDataframe = stockinfo[1]
    path = "C:\\Users\\suman\\Desktop\\Stocks\\{}.csv".format(ticker)
    save_data(stockDataframe, path)
    # print(stockinfo[0] + ' size : ' + str(stockinfo[1].size))
    fig = RunScreener(stockDataframe, ticker)
    img = "C:\\Users\\suman\\Desktop\\Stocks\\{}.png".format(ticker)
    fig.savefig(img)
