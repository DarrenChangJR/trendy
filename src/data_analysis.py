from datetime import date
import pandas as pd
from logging import getLogger

logger = getLogger()

def alpha(df: pd.DataFrame, benchmark_df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Calculating alpha, symbol has {len(df)} rows, benchmark has {len(benchmark_df)} rows")
    assert "close" in df.columns, "\"close\" column not found in dataframe"
    assert "close" in benchmark_df.columns, "\"close\" column not found in benchmark's dataframe"

    df = df.join(benchmark_df, how="left", rsuffix="_benchmark")
    df["alpha"] = df["delta"] - df["delta_benchmark"]
    logger.info(f"Calculated alpha, left with {df["alpha"].count()} rows of usable alpha data")

    return df

def min_mse(df: pd.DataFrame, principal_event_date: date, dates: list[date], pre_event: int, post_event: int, max_offset: int) -> pd.DataFrame:
    logger.info(f"Calculating minimum MSE between principal ({principal_event_date}) and {len(dates)} events")
    latest_index = df.index.get_indexer([pd.Timestamp(principal_event_date)], "nearest")[0]
    latest_event_timeline = df.iloc[latest_index - pre_event:latest_index + post_event + 1]
    latest_event_timeline_alpha = latest_event_timeline["alpha"].to_numpy()
    logger.info(f"Principal event timeline: {latest_event_timeline.iloc[0].name.date()} - {latest_event_timeline.iloc[-1].name.date()}")

    min_mse = pd.DataFrame(columns=["mse", "offset"], index=dates)
    for event_date in dates:
        event_index = df.index.get_indexer([pd.Timestamp(event_date)], "nearest")[0]
        start = event_index - pre_event
        end = event_index + post_event + 1
        for offset in range(-max_offset, max_offset + 1):
            assert start + offset >= 0, f"start + offset = {start + offset} < 0, caused by date {event_date}"
            assert end + offset <= len(df), f"end + offset = {end + offset} > {len(df)}, caused by date {event_date}"
            mse = ((latest_event_timeline_alpha - df.iloc[start + offset:end + offset]["alpha"].to_numpy()) ** 2).mean()
            if pd.isna(min_mse.loc[event_date, "mse"]) | (mse < min_mse.loc[event_date, "mse"]):
                min_mse.loc[event_date] = mse, offset
            elif mse == min_mse.loc[event_date, "mse"]:
                min_mse.loc[event_date] = mse, min(min_mse.loc[event_date, "offset"], offset)
    
    return min_mse
