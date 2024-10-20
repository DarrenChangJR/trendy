from datetime import date, timedelta
import os

import utils
from twelvedata import TwelveData
from keys import TWELVE_DATA_KEY

def _fetch_symbol(symbol: str, event_dates: list[date], pre_event: int, post_event: int) -> None:
    filename = utils.get_filename(symbol, event_dates, pre_event, post_event)
    data_dir = utils.get_dir('data')

    if filename in os.listdir(data_dir):
        print(f"Exists: {filename}")

    else:
        start = min(event_dates)
        end = max(event_dates)
        
        print(f"Initiating fetch: {symbol} {start} {end}")
        twelvedata = TwelveData(TWELVE_DATA_KEY)
        with open(f"{data_dir}/{filename}", "a") as file:
            # write header
            file.write("date;open;high;low;close;volume\n")
            i = start
            while i < end:
                data = twelvedata.get_time_series(symbol, i, min(i + timedelta(days=6352), end), "1day", format="csv", filename=filename)
                i += timedelta(days=6352)
                file.write(data[data.index("\n") + 1:])
        print(f"Fetch Complete: {symbol} {start} {end}")

def fetch_symbols(symbols: list[str], event_dates: list[date], pre_event: int, post_event: int) -> None:
    for symbol in symbols:
        _fetch_symbol(symbol, event_dates, pre_event, post_event)
