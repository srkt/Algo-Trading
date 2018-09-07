import pandas as pd

from technical.screener import EmaReversion, Bollinger, StochasticOscillator, Macd, Vwap, Rsi, Screener

def RunScreener(df, close_column='close', volume_column='volume'):
    if not isinstance(df, pd.DataFrame):
        raise Exception('Dataframe expected')

    # create screener
    screener = Screener(df)

    # Stratagies
    emrev = EmaReversion(df, close_column, 12, 21)
    bb = Bollinger(df, close_column, 14)
    sco = StochasticOscillator(df, 14, name=close_column)
    mcd = Macd(df, close_column)
    vwap = Vwap(df, close_column, vol_col_name=volume_column)
    rsi = Rsi(df, name=close_column)

    # add to screener
    screener.add_strategy(emrev)
    screener.add_strategy(bb)
    screener.add_strategy(sco)
    screener.add_strategy(rsi)
    screener.add_strategy(mcd)
    screener.add_strategy(vwap)

    results = screener.run()

    result_list = []

    for result in results:
        output = {
            'strategy': result.strategy_name,
            'signal': result.buy_sell,
            'weight': result.weight
        }
        result_list.append(output)
        # print('Strategy : ' + result.strategy_name + ', signal : ' + result.buy_sell + ', weight: ' + str(
        #     result.weight))

    # print('Current price:' + str(df[close_column][-1]))
    return result_list
