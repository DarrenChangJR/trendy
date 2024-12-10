from datetime import date
import pandas as pd
from logging import getLogger

logger = getLogger()

def alpha(df: pd.DataFrame, benchmark_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the alpha values by subtracting the benchmark's delta from the symbol's delta.

    Args:
        df (pd.DataFrame): DataFrame containing the symbol's data with a "delta" column.
        benchmark_df (pd.DataFrame): DataFrame containing the benchmark's data with a "delta" column.

    Returns:
        pd.DataFrame: DataFrame with an additional "alpha" column representing the calculated alpha values.

    Raises:
        AssertionError: If the "delta" column is not found in either DataFrame.
    """
    logger.info(f"Calculating alpha, symbol has {len(df)} rows, benchmark has {len(benchmark_df)} rows")
    assert "delta" in df.columns, "\"delta\" column not found in dataframe"
    assert "delta" in benchmark_df.columns, "\"delta\" column not found in benchmark's dataframe"

    df = df.join(benchmark_df, how="left", rsuffix="_benchmark")
    df["alpha"] = df["delta"] - df["delta_benchmark"]
    logger.info(f"Calculated alpha, left with {df["alpha"].count()} rows of usable alpha data")

    return df

def min_mse(df: pd.DataFrame, principal_event_date: date, dates: list[date], pre_event: int, post_event: int, max_offset: int) -> pd.DataFrame:
    """
    Calculates the minimum mean squared error (MSE) between the principal event and other events.

    Args:
        df (pd.DataFrame): DataFrame containing the symbol's data with an "alpha" column.
        principal_event_date (date): The date of the principal event.
        dates (list[date]): List of dates for other events to compare against the principal event.
        pre_event (int): Number of days before the event to include in the analysis.
        post_event (int): Number of days after the event to include in the analysis.
        max_offset (int): Maximum number of days to offset the event date by.

    Returns:
        pd.DataFrame: DataFrame with columns "mse" and "offset" representing the minimum MSE and corresponding offset for each event date.

    Raises:
        AssertionError: If the end of the sliding window plus offset exceeds the length of the DataFrame.
    """
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
            assert end + offset <= len(df), f"end + offset = {end + offset} > {len(df)}, caused by date {event_date}"
            # start of sliding window is not in range, i.e. symbol has not traded yet
            if start + offset < 0:
                min_mse.loc[event_date] = pd.NA, offset
                continue
            # calculate mse and retain minimum, or if equal, then retain offset closest to 0
            mse = ((latest_event_timeline_alpha - df.iloc[start + offset:end + offset]["alpha"].to_numpy()) ** 2).mean()
            if pd.isna(min_mse.loc[event_date, "mse"]) | (mse < min_mse.loc[event_date, "mse"]):
                min_mse.loc[event_date] = mse, offset
            elif mse == min_mse.loc[event_date, "mse"]:
                min_mse.loc[event_date, "offset"] = min(abs(min_mse.loc[event_date, "offset"]), abs(offset))
    
    return min_mse
