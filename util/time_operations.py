import datetime as dt
from tzlocal import get_localzone
import pandas as pd

def toTs(ms):
    s = ms / 1000.0
    return dt.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')


def toLocalTimeZone(ms):
    mytz = get_localzone()
    return pd.to_datetime(ms, unit='ms').dt.tz_localize('UTC').dt.tz_convert(mytz)
