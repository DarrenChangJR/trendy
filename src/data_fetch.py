from datetime import date, timedelta
from logging import getLogger

import utils
from twelvedata import TwelveData
from keys import TWELVE_DATA_KEY

logger = getLogger()

def fetch_to_csv(symbol: str, start: date, end: date) -> str:
    filepath, _ = utils.data_filepath(symbol, start, end, "csv")
    logger.info(f"Fetching data: {symbol} {start} {end}")
    twelvedata = TwelveData(TWELVE_DATA_KEY)
    with open(filepath, "a") as file:
        file.write("date;open;high;low;close;volume\n")
        i = start
        while i < end:
            td = min(i + timedelta(days=6352), end)
            logger.debug(f"Fetching data: {i} to {td}")
            data = twelvedata.time_series(symbol, i, td, "1day", format="csv")
            i = td
            file.write(data[data.index("\n") + 1:])
    logger.info(f"Fetch complete: {filepath}")
    return filepath
