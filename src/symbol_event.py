from datetime import date, timedelta

import utils
import data_fetch
import data_analysis


class SymbolEvent:
    
    def __init__(self, symbol: str, event_dates: list[date], pre_event: int, post_event: int, max_offset: int) -> None:
        assert len(event_dates) > 0
        for event_date in event_dates:
            assert isinstance(event_date, date)
        assert pre_event >= 0
        assert post_event >= 0
        assert max_offset >= 0
        
        self.symbol = symbol
        self.event_dates = sorted(event_dates, reverse=True)
        self.pre_event = pre_event
        self.post_event = post_event
        self.max_offset = max_offset
        self.start = min(event_dates) - timedelta(days=(pre_event + max_offset) * 1.6)
        self.end = max(event_dates) + timedelta(days=(post_event + max_offset) * 1.6)

        assert self.end <= date.today()

        self._data_fetch_sequence()
        self._data_analysis_sequence()

    def _data_fetch_sequence(self):
        self.csv_filepath, csv_exists = utils.data_filepath(self.symbol, self.start, self.end, "csv")
        if not csv_exists:
            data_fetch.fetch_to_csv(self.symbol, self.start, self.end)
        
    def _data_analysis_sequence(self):
        self.raw_df = data_analysis.raw_df(self.csv_filepath)
        self.raw_tensor = data_analysis.raw_tensor(self.raw_df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
        self.delta_tensor = data_analysis.delta_tensor(self.raw_tensor)

    def normalise_against(self, benchmark_symbol: str):
        self.benchmark_symbol = benchmark_symbol
        benchmark_csv_filepath = data_fetch.fetch_to_csv(benchmark_symbol, self.start, self.end)
        benchmark_delta_pt_filepath, benchmark_delta_pt_file_exists = utils.data_filepath(benchmark_symbol, self.start, self.end, "pt")
        if not benchmark_delta_pt_file_exists:
            benchmark_raw_df, _ = data_analysis.raw_df(benchmark_csv_filepath)
            benchmark_raw_tensor = data_analysis.raw_tensor(benchmark_raw_df)
            benchmark_delta_tensor = data_analysis.delta_tensor(benchmark_raw_tensor)
            data_analysis.torch_save(benchmark_delta_pt_filepath, benchmark_delta_tensor)
        else:
            benchmark_delta_tensor = data_analysis.torch_load(benchmark_delta_pt_filepath)
        self.delta_tensor = data_analysis.normalise_against(self.delta_tensor, benchmark_delta_tensor)
    
    def min_mse(self):
        return data_analysis.min_mse(self.delta_tensor, self.max_offset)