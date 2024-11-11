from datetime import date, timedelta
from logging import getLogger
from io import StringIO
import pandas as pd

import utils
from twelvedata import TwelveData
from keys import TWELVE_DATA_KEY

logger = getLogger()

def generate_df(symbol: str, event_dates: list[date], post_event: int) -> pd.DataFrame:
    twelvedata = TwelveData(TWELVE_DATA_KEY)
    
    csv_path, csv_exists = utils.file_path(f"data/{symbol}.csv")
    if csv_exists:
        logger.info(f"Exists local data, reading from {csv_path}")
        df = pd.read_csv(csv_path, parse_dates=["date"], index_col="date")
        if _df_sufficient(df, event_dates, post_event):
            logger.info("Local data is sufficient")
            return df
        logger.info("Local data is not sufficient, fetching more data")
        new_df = _time_series_df(twelvedata, symbol, df.iloc[-1].name.date() + timedelta(days=1))
        df = df.append(new_df)
    else:
        logger.info(f"Fetching: {symbol}")
        earlist_date = twelvedata.earliest_timestamp(symbol)
        df = _time_series_df(twelvedata, symbol, earlist_date)
    
    df = df[~df.index.duplicated(keep="first")]
    df.sort_index(inplace=True)
    df["delta"] = df["close"].diff() / df.shift(1)["close"]
    
    assert _df_sufficient(df, event_dates, post_event), "The latest event timeline has not completed yet! Consider reducing post_event."
    
    logger.info(f"Writing for future use: {csv_path}")
    df.to_csv(csv_path)
    return df

def _time_series_df(twelvedata: TwelveData, symbol: str, start_date: date) -> pd.DataFrame:
    close = "date;open;high;low;close;volume\n"
    
    end_date = start_date
    while end_date < date.today():
        start_date = end_date
        end_date += timedelta(weeks=988)
        new_close = twelvedata.time_series(symbol, start_date, end_date)
        close += new_close[new_close.index("\n") + 1:]

    return pd.read_csv(
        StringIO(close),
        sep=";",
        usecols=["date", "close"],
        parse_dates=["date"],
        index_col="date"
    )

def _df_sufficient(df: pd.DataFrame, event_dates: list[date], post_event: int) -> bool:
    latest_event_index = df.index.get_indexer([pd.Timestamp(event_dates[0])], "nearest")[0]
    return (latest_event_index + post_event) < len(df)
