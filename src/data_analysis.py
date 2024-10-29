from datetime import date
import pandas as pd
from logging import getLogger

logger = getLogger()

def add_alpha(df: pd.DataFrame, benchmark_df: pd.DataFrame) -> pd.DataFrame:
    assert "close" in df.columns, "\"close\" column not found in dataframe"
    assert "close" in benchmark_df.columns, "\"close\" column not found in benchmark's dataframe"
    assert df.index.isin(benchmark_df.index).all(), "Not all dates in dataframe are in benchmark's dataframe, consider using a different benchmark"

    df = df.join(benchmark_df, how="left", rsuffix="_benchmark")
    df["alpha"] = df["delta"] - df["delta_benchmark"]
    logger.info(f"Calculated alpha for {len(df)} rows")

    return df

def min_mse(df: pd.DataFrame, event_dates: list[date], pre_event: int, post_event: int, max_offset: int) -> pd.DataFrame:
    logger.info(f"Calculating min_mse for {len(event_dates)} events")
    latest_index = df.index.get_indexer([pd.Timestamp(event_dates[0])])[0]
    latest_event_timeline = df.iloc[latest_index - pre_event:latest_index + post_event + 1]["alpha"].to_numpy()
    
    min_mse = pd.DataFrame(columns=["mse", "offset"], index=event_dates[1:])
    for event_date in event_dates[1:]:
        event_index = df.index.get_indexer([pd.Timestamp(event_date)], method="nearest")[0]
        start = event_index - pre_event
        end = event_index + post_event + 1
        for offset in range(-max_offset, max_offset + 1):
            assert start + offset >= 0, f"start + offset = {start + offset} < 0, caused by date {event_date}"
            assert end + offset <= len(df), f"end + offset = {end + offset} > {len(df)}, caused by date {event_date}"
            mse = ((latest_event_timeline - df.iloc[start + offset:end + offset]["alpha"].to_numpy()) ** 2).mean()
            if pd.isna(min_mse.loc[event_date, "mse"]) | (mse < min_mse.loc[event_date, "mse"]):
                min_mse.loc[event_date] = mse, offset
            elif mse == min_mse.loc[event_date, "mse"]:
                min_mse.loc[event_date] = mse, min(min_mse.loc[event_date, "offset"], offset)
    
    return min_mse
