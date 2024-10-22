from datetime import date
import torch
import pandas as pd

def raw_df(csv_filepath: str, event_dates: list[date]) -> tuple[pd.DataFrame, list[int]]:
    df = pd.read_csv(csv_filepath, sep=";", usecols=["date", "close"], parse_dates=["date"], index_col="date")
    df.sort_index(ascending=False, inplace=True)
    event_indices = df.index.get_indexer_for(event_dates)
    return df, event_indices

def raw_tensor(df: pd.DataFrame) -> tuple[torch.Tensor, list[int]]:
    raw_tensor = torch.tensor(df["close"].values).cuda()
    return raw_tensor

def delta_tensor(raw_tensor: torch.Tensor) -> torch.Tensor:
    return torch.div(raw_tensor.diff(), raw_tensor[1:])

def normalise_against(raw_tensor: torch.Tensor, benchmark_tensor: torch.Tensor) -> torch.Tensor:
    return torch.div(raw_tensor, benchmark_tensor)

# receive tensor, event_date_index, pre, post, max_offset
def mse_loss(tensor: torch.Tensor, start1: int, end1: int, start2: int, end2: int) -> torch.NumberType:
    return torch.nn.functional.mse_loss(tensor[start1:end1], tensor[start2:end2]).item()

def find_min_mse_loss(tensor: torch.Tensor, indices: list[int], pre: int, post: int, max_offset: int) -> list[tuple[int, torch.NumberType]]:
    """
    Return is a list of length len(indices)-1 where each element is a 2-tuple of (offset where min_mse is, value of min_mse)
    """
    # compute the mse_loss on all row pairs in parallel
    mse_losses = torch.zeros((len(indices)-1, max_offset+1))
    


def torch_save(filepath: str, tensor: torch.Tensor):
    torch.save(tensor, filepath)
    print(f"Saved tensor to {filepath}")

def torch_load(filepath: str) -> torch.Tensor:
    print(f"Loaded tensor from {filepath}")
    return torch.load(filepath)
