import torch
import pandas as pd
from datetime import date

import utils


class SymbolEvent:
    _loss_function = torch.nn.MSELoss()
    
    def __init__(self, symbol: str, event_dates: list[date], pre_event: int, post_event: int) -> None:
        self.symbol = symbol
        self.event_dates = event_dates
        self.pre_event = pre_event
        self.post_event = post_event
        self.tensor = self._csv_to_tensor()

    def _csv_to_tensor(self) -> torch.Tensor:
        data_dir = utils.get_dir('data')
        filename = utils.get_filename(self.symbol, self.event_dates, self.pre_event, self.post_event)
        filename = "sample.csv"
        
        df = pd.read_csv(f"{data_dir}/{filename}", sep=";", usecols=["date", "close"], parse_dates=["date"], index_col="date")
        df.sort_index(ascending=False, inplace=True)
        raw_tensor = torch.tensor(df["close"].values).cuda()
        change_tensor = torch.div(raw_tensor.diff(), raw_tensor[1:])
        print(change_tensor)