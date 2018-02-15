from tzlocal import get_localzone
import datetime as dt
import numpy as np
from technical.indicators import get_alphabeta
from trading.stock_exchange import StockExchange
from util.utility import RunScreener, py_mail
import pandas as pd

stocks = ['SQ', 'MSFT', 'AMZN', 'WB']
columns = ['strategy', 'signal', 'weight']
beta_periods = [2, 5, 10, 15]


def generate_stock_alerts():
    print('Started generating stock alerts')
    local_tz = get_localzone()
    se = StockExchange()
    to_date = dt.datetime.now(local_tz)
    from_date = to_date - dt.timedelta(days=30)
    result_str = ''

    stock_list = se.get_data(stocks, from_date, to_date)

    for stock in stock_list:
        data_array = stock[1]
        res = RunScreener(data_array, close_column='Close', volume_column='Volume')
        result_str = result_str + '<div><h1>' + str(stock[0]) + ' : ' + str(stock[1]['Close'][-1]) + '</h1></div>'

        result_str = result_str + '<table style="border:1px solid black;font-size:14px;margin-bottom:10px">'
        result_str = result_str + '<tr style="border:1px solid black;"><th>Period(days)</th><th>Change (per stock)</th><th>Mean Change</th></tr>'
        for beta_period in beta_periods:
            # nth value for normalizing
            nth_value = data_array['Close'][-beta_period]
            # normalized values
            n_values = data_array[-beta_period:]['Close']
            normalized_change = (n_values / nth_value)
            pct_change = data_array['Close'].tail(beta_period).pct_change(1)

            # a, b = get_alphabeta(np.arange(1, beta_period + 1, 1),
            #                      pct_change[1:])
            b = np.mean(pct_change[1:])
            result_str = result_str + '<tr style="border:1px solid black;"><td style="border:1px solid black;">' + str(
                beta_period) + '</td><td style="border:1px solid black;">' + str(
                normalized_change[-1]) + '</td><td style="border:1px solid black;">' + str(b) + '</td></tr>'

        result_str = result_str + '</table>'
        result_str = result_str + '<div>' + pd.DataFrame(res, columns=columns).to_html() + '</div>'

    print('sending mail...')
    py_mail('Stock Alert', result_str, 'obsoleteattribute@gmail.com,srk36@yahoo.com', 'mytrademailer@gmail.com')

    print('completed running stock alerts')
