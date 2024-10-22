from datetime import date, timedelta

import utils
from twelvedata import TwelveData
from keys import TWELVE_DATA_KEY

def fetch_to_csv(symbol: str, start: date, end: date) -> str:
    filepath, file_exists = utils.data_filepath(symbol, start, end, "csv")
    
    if file_exists:
        print(f"Exists: {symbol} {start} {end}")
        return filepath
    
    print(f"Initiating fetch: {symbol} {start} {end}")
    twelvedata = TwelveData(TWELVE_DATA_KEY)
    with open(filepath, "a") as file:
        file.write("date;open;high;low;close;volume\n")
        i = start
        while i < end:
            data = twelvedata.time_series(symbol, i, min(i + timedelta(days=6352), end), "1day", format="csv")
            i += timedelta(days=6352)
            file.write(data[data.index("\n") + 1:])
    print(f"Fetch Complete: {symbol} {start} {end}")
    return filepath