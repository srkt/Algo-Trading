import pandas as pd
import numpy as np


def get_rsi(data, period, name):
    if not name:
        raise Exception('invalid column name')

    if not period:
        period = 14

    if not isinstance(data, pd.DataFrame):
        raise Exception('Invalid data passed , expecting pandas data frame')

    up_avg_str = 'up_avg_' + str(period)  # up average string 
    down_avg_str = 'down_avg_' + str(period)  # down average string

    data['diff'] = data[name] - data[name].shift(1)

    data['up'] = np.where(data['diff'] > 0, data['diff'], 0)
    data['down'] = np.where(data['diff'] > 0, 0, -data['diff'])

    data[up_avg_str] = data['up'].rolling(period).mean()
    data[down_avg_str] = data['down'].rolling(period).mean()

    data['relative_strength'] = data[up_avg_str] / data[down_avg_str]

    data['rsi'] = 100 - (100 / (data['relative_strength'] + 1))

    data = data[['close', 'up', 'down', 'relative_strength', 'rsi']]

    return data


def Ema(data, name, period):
    if not name:
        raise Exception('invalid column name')

    if not period:
        period = 14

    if not isinstance(data, pd.DataFrame):
        raise Exception('Invalid data passed , expecting pandas data frame')

#    return pd.ewma(data[name], span=period)
    return data[name].ewm(com=0.5).mean()


def Macd(data, name, minperiod, maxperiod, signalperiod):
    if not name:
        raise Exception('invalid column name')

    if not minperiod:
        minperiod = 12

    if not maxperiod:
        maxperiod = 21

    if not signalperiod:
        signalperiod = 9

    if not isinstance(data, pd.DataFrame):
        raise Exception('Invalid data passed , expecting pandas data frame')

    minema = Ema(data, name, minperiod)
    maxema = Ema(data, name, maxperiod)

    macd = minema - maxema

    # signal = pd.ewma(macd, span=signalperiod)
    signal = macd.ewm(com=0.5).mean()

    return macd, signal


def RollingStDev(data, name, period):
    if not isinstance(data, pd.DataFrame):
        raise Exception('expected pandas dataframe')

    return pd.rolling_std(data[[name]], window=period)


def RollingStDev(data, name, period):
    if not isinstance(data, pd.DataFrame):
        raise Exception('expected pandas dataframe')

    return pd.rolling_std(data[[name]], window=period)


def Mean(data, name):
    if not isinstance(data, pd.DataFrame):
        raise Exception('expected pandas dataframe')

    return data[[name]].mean()


def get_alphabeta(x, y, degree=1):
    if (x is None or y is None):
        raise Exception('invalid parameters passed')
    print(x)
    print(y)
    beta, alpha = np.polyfit(x, y, deg=degree)
    return alpha, beta
