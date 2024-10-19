from twelvedata import TwelveData
from datetime import date, timedelta
import os

from keys import TWELVE_DATA_KEY


def data_fetch(symbol: str, event_dates: list[date], pre_event: int, post_event: int) -> bool:
    
    start = min(event_dates) - timedelta(days=pre_event * 1.5)
    end = max(event_dates) + timedelta(days=post_event * 1.5)
    filename = f"{symbol} {start.strftime("%Y-%m-%d")} {end.strftime("%Y-%m-%d")}.csv"
    
    os.chdir("data")
    filenames = os.listdir()
    if filename in filenames:
        with open(f"./{filename}", "r") as file:
            data = file.read()

    else:
        twelvedata = TwelveData(TWELVE_DATA_KEY)
        while start < end:
            data = twelvedata.get_time_series(symbol, start, min(start + timedelta(days=6352), end), "1day", format="csv")
            start += timedelta(days=5000)
            with open(f"./{filename}", "a") as file:
                file.write(data)
        