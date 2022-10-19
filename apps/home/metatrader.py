import datetime                 
import pytz                     
import pandas            as pd  
import MetaTrader5       as mt5 
import os, environ
from core.settings import BASE_DIR



env = environ.Env(
    DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

mt5.initialize(login=env('mt5Login'), password=env('mt5Password'), server=env('mt5Server'))

version = mt5.version()


def get_quotes(asset = "EURUSD", time_frame = None, year = 2022, month = 1, day = 1, hour = 0, minute=0, seconds=0):
        
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    
    timezone = pytz.timezone("Europe/Kiev")
    
    utc_from = datetime.datetime(year, month, day, hour=hour, minute=minute, second=seconds, tzinfo = timezone)

    if time_frame == 'M1':
        # data = mt5.copy_ticks_from(asset, utc_from, 135, mt5.COPY_TICKS_ALL)
        data = mt5.copy_ticks_range(asset, utc_from - datetime.timedelta(minutes=120), utc_from, mt5.COPY_TICKS_ALL)
        tick_data = pd.DataFrame(data)
        tick_data = tick_data.assign(time = pd.to_datetime(tick_data['time'], unit = 's')).set_index('time').resample('1min')['ask'].ohlc()
    elif time_frame == 'S1':
        # data = mt5.copy_ticks_from(asset, utc_from, 180, mt5.COPY_TICKS_ALL)
        data = mt5.copy_ticks_range(asset, utc_from, utc_from + datetime.timedelta(seconds=180), mt5.COPY_TICKS_ALL)
        tick_data = pd.DataFrame(data)
        tick_data = tick_data.assign(time = pd.to_datetime(tick_data['time'], unit = 's')).set_index('time').resample('1s')['ask'].ohlc()
    return tick_data.to_json(orient="split")


def mass_import(asset, horizon, year, month, day, hour, minute):
    data = get_quotes(asset, horizon, year, month, day, hour, minute)
    return data
