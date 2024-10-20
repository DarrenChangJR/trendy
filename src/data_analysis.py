import torch
from pandas import read_csv
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
        df = read_csv(f"{data_dir}/{filename}", sep=";", usecols=["date", "close"])
        tensor = torch.tensor(df["close"].values).cuda()
        print(tensor.device)
        return tensor