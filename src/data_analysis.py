from datetime import date, timedelta
import torch
import pandas as pd
from logging import getLogger

logger = getLogger()

def raw_df(csv_filepath: str) -> pd.DataFrame:
    logger.info(f"Reading {csv_filepath}")
    df = pd.read_csv(
        csv_filepath,
        sep=";",
        usecols=["date", "close"],
        parse_dates=["date"],
        index_col="date"
    )
    df.sort_index(inplace=True)
    return df

def raw_tensor(df: pd.DataFrame, event_dates: list[date], pre_event: int, post_event: int, max_offset: int) -> torch.Tensor:
    raw_tensor = torch.empty(len(event_dates), pre_event + post_event + 2 * max_offset + 1)
    logger.info(f"Creating tensor of shape {raw_tensor.shape}")
    for i, event_date in enumerate(event_dates):
        event_timestamp = pd.Timestamp(event_date)
        index = df.index.get_loc(event_timestamp)
        logger.debug(f"Event date: {event_date}, indices: [{index - pre_event - max_offset} to {index + post_event + max_offset + 1})")
        raw_tensor[i] = torch.tensor(df.iloc[index - pre_event - max_offset:index + post_event + max_offset + 1]["close"].values)
    
    if torch.cuda.is_available():
        logger.info("CUDA is available, transferring tensor to GPU")
        raw_tensor = raw_tensor.cuda()
    else:
        logger.info("CUDA is not available, retaining tensor in CPU")
    return raw_tensor

def delta_tensor(raw_tensor: torch.Tensor) -> torch.Tensor:
    return torch.div(raw_tensor.diff(), raw_tensor[:, :-1])

def normalise_against(raw_tensor: torch.Tensor, benchmark_tensor: torch.Tensor) -> torch.Tensor:
    return torch.div(raw_tensor, benchmark_tensor)

def min_mse(tensor: torch.Tensor, max_offset: int):
    latest_event_timeline = tensor[0, max_offset:-max_offset]
    mse_losses = torch.stack([
        ((latest_event_timeline - tensor[1:, offset:offset - max_offset * 2]) ** 2).mean(dim=1)
        for offset in range(0, 2 * max_offset)
    ], dim=1)
    return mse_losses.min(dim=1)

def torch_save(filepath: str, tensor: torch.Tensor):
    torch.save(tensor, filepath)
    logger.info(f"Saved tensor to {filepath}")

def torch_load(filepath: str) -> torch.Tensor:
    logger.info(f"Loading tensor from {filepath}")
    return torch.load(filepath)
