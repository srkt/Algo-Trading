import datetime as dt
import numpy as np
import pandas as pd
from binance.client import Client
from tzlocal import get_localzone

import util.keys as util
from technical.indicators import get_alphabeta
from trading.binance_api import Binance
from util.utility import py_mail, RunScreener

coin_pairs = ['BTCETH', 'BTCXRP', 'BTCADA', 'BTCXVG', 'BTCXLM', 'BTCTRX']
columns = ['strategy', 'signal', 'weight']
r_df = pd.DataFrame(columns=columns)


def get_datetime():
    local_tz = get_localzone()
    return dt.datetime.now(local_tz)


def get_binance_data(coin_pair):
    key, secret = util.ks()
    b_inst = Binance(key, secret)
    to_date = get_datetime()
    from_date = to_date - dt.timedelta(days=1)
    df = b_inst.get_data(coin_pair, from_date, to_date, interval=Client.KLINE_INTERVAL_1HOUR)
    return df


# deprecated
def generate_crypto_alerts_old():
    print('Started generating alerts')
    r_list = []
    for coin in coin_pairs:
        df = get_binance_data(coin)
        res = RunScreener(df)
        r_list.extend(res)

    rdf = pd.DataFrame(r_list, columns=columns)

    print('converting data to text')
    msg = rdf.to_html()

    print('sending mail...')
    py_mail('Crypto Alert', msg, 'obsoleteattribute@gmail.com,srk36@yahoo.com', 'mytrademailer@gmail.com')

    print('completed running alerts')


beta_periods = [2, 5, 10]


def generate_crypto_alerts():
    print('Started generating alerts')
    to_date = get_datetime()
    coin_pair_tuples = get_binance_data(coin_pairs)
    result_str = ''
    for coin_pair_tuple in coin_pair_tuples:
        data_array = coin_pair_tuple[1]
        res = RunScreener(data_array)
        result_str = result_str + '<div><h1>' + str(coin_pair_tuple[0]) + ' : ' + str(
            data_array['close'][-1]) + '</h1></div>'
        result_str = result_str + '<table style="border:1px solid black;font-size:14px;margin-bottom:10px">'
        result_str = result_str + '<tr style="border:1px solid black;"><th>Period (hrs)</th><th>Change (per coin)</th><th>Mean Change</th></tr>'
        for beta_period in beta_periods:
            # nth value for normalizing
            nth_value = data_array['close'][-beta_period]
            # normalized values
            n_values = data_array[-beta_period:]['close']
            normalized_change = (n_values / nth_value)

            pct_change = data_array['close'].tail(beta_period).pct_change(1)

            # a, b = get_alphabeta(np.arange(1, beta_period + 1, 1), data_array['close'].tail(beta_period + 1).pct_change(1)[1:])
            b = np.mean(pct_change[1:])
            result_str = result_str + '<tr style="border:1px solid black;"><td style="border:1px solid black;">' + str(
                beta_period) + '</td><td style="border:1px solid black;">' + str(
                normalized_change[-1]) + '</td><td style="border:1px solid black;">' + str(
                b) + '</td></tr>'

        result_str = result_str + '</table>'
        result_str = result_str + '<div>' + pd.DataFrame(res, columns=columns).to_html() + '</div>'

    print('sending mail...')
    py_mail('Crypto Alert', result_str, 'obsoleteattribute@gmail.com,srk36@yahoo.com', 'mytrademailer@gmail.com')

    print('completed running alerts')
