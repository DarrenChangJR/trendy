from datetime import date, timedelta
from logging import getLogger
from io import StringIO
import pandas as pd

import utils
from twelvedata import TwelveData
from keys import TWELVE_DATA_KEY

logger = getLogger()

def generate_df(symbol: str, event_dates: list[date], post_event: int, max_offset: int) -> pd.DataFrame:
    twelvedata = TwelveData(TWELVE_DATA_KEY)
    
    csv_path, csv_exists = utils.file_path(f"data/{symbol}.csv")
    if csv_exists:
        logger.info(f"Exists local data, reading from {csv_path}")
        df = pd.read_csv(csv_path, parse_dates=["date"], index_col="date")
        if _df_sufficient(df, event_dates, post_event, max_offset):
            return df
        logger.info("Local data is not sufficient, fetching more data")
        new_df = _fetch_from(df.iloc[-1].name.date() + timedelta(days=1))
        df = df.append(new_df)
    else:
        logger.info(f"Fetching: {symbol}")
        earlist_date = twelvedata.earliest_timestamp(symbol)
        df = _fetch_from(twelvedata, symbol, earlist_date)
    
    assert _df_sufficient(df, event_dates, post_event, max_offset), "The latest event timeline is not complete yet! Consider reducing max_offset and/or post_event."
    
    df.sort_index(inplace=True)
    logger.info(f"Writing for future use: {csv_path}")
    df.to_csv(csv_path)
    return df

def _fetch_from(twelvedata: TwelveData, symbol: str, start_date: date) -> pd.DataFrame:
    data = "date;open;high;low;close;volume\n"
    next_page = True
    while next_page:
        new_data = twelvedata.time_series(symbol, start_date)
        next_page = new_data.count("\n") == 5000
        data += new_data[new_data.index("\n") + 1:]
    
    return pd.read_csv(
        StringIO(data),
        sep=";",
        usecols=["date", "close"],
        parse_dates=["date"],
        index_col="date"
    )

def _df_sufficient(df: pd.DataFrame, event_dates: list[date], post_event: int, max_offset: int) -> bool:
    latest_event_index = df.index.get_loc(pd.Timestamp(event_dates[0]))
    return (latest_event_index + post_event + max_offset) < len(df)
