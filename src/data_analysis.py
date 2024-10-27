from datetime import date
import pandas as pd
# import numpy as np
from logging import getLogger

logger = getLogger()

def df(csv_filepath: str, benchmark_csv_filepath: str) -> pd.DataFrame:
    df = _raw_df(csv_filepath)
    benchmark_df = _raw_df(benchmark_csv_filepath)
    df = df.join(benchmark_df, how="left", rsuffix="_benchmark")
    
    df["delta"] = df["close"].diff() / df.shift(1)["close"]
    df["delta_benchmark"] = df["close_benchmark"].diff() / df.shift(1)["close_benchmark"]
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

def _raw_df(csv_filepath: str) -> pd.DataFrame:
    logger.info(f"Reading {csv_filepath}")
    raw_df = pd.read_csv(
        csv_filepath,
        sep=";",
        usecols=["date", "close"],
        parse_dates=["date"],
        index_col="date"
    )
    raw_df.sort_index(inplace=True)
    logger.info(f"Read {len(raw_df)} rows into DataFrame")
    return raw_df

# def raw_tensor(df: pd.DataFrame, event_dates: list[date], pre_event: int, post_event: int, max_offset: int) -> torch.Tensor:
#     raw_tensor = torch.empty(len(event_dates), pre_event + post_event + 2 * max_offset + 1)
#     logger.info(f"Creating tensor of shape {raw_tensor.shape}")
#     for i, event_date in enumerate(event_dates):
#         event_timestamp = pd.Timestamp(event_date)
#         index = df.index.get_loc(event_timestamp)
#         logger.debug(f"Event date: {event_date}, indices: [{index - pre_event - max_offset} to {index + post_event + max_offset + 1})")
#         raw_tensor[i] = torch.tensor(df.iloc[index - pre_event - max_offset:index + post_event + max_offset + 1]["close"].values)
    
#     if torch.cuda.is_available():
#         logger.info("CUDA is available, transferring tensor to GPU")
#         raw_tensor = raw_tensor.cuda()
#     else:
#         logger.info("CUDA is not available, retaining tensor in CPU")
#     return raw_tensor

# def delta_tensor(raw_tensor: torch.Tensor) -> torch.Tensor:
#     return torch.div(raw_tensor.diff(), raw_tensor[:, :-1])

# def min_mse(tensor: torch.Tensor, max_offset: int):
#     latest_event_timeline = tensor[0, max_offset:-max_offset]
#     mse_losses = torch.stack([
#         ((latest_event_timeline - tensor[1:, offset:offset - max_offset * 2]) ** 2).mean(dim=1)
#         for offset in range(0, 2 * max_offset)
#     ], dim=1)
#     return mse_losses.min(dim=1)

# def torch_save(filepath: str, tensor: torch.Tensor):
#     torch.save(tensor, filepath)
#     logger.info(f"Saved tensor to {filepath}")

# def torch_load(filepath: str) -> torch.Tensor:
#     logger.info(f"Loading tensor from {filepath}")
#     return torch.load(filepath)
