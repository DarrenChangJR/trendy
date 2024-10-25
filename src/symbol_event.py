from datetime import date, timedelta

import utils
import data_fetch
import data_analysis


class SymbolEvent:

    def __init__(self, symbol: str, event_dates: list[date], pre_event: int, post_event: int, max_offset: int, benchmark_symbol: str | None = None) -> None:
        """
        Args:
            symbol (str): The symbol of the stock to analyze.
            event_dates (list[date]): The dates of the events to analyze.
            pre_event (int): The number of days before the event to include in trend analysis.
            post_event (int): The number of days after the event to include in trend analysis.
            max_offset (int): The maximum number of days to offset the event date by, used by event dates other than the latest one.
            benchmark_symbol (str | None): The symbol to subtract from the symbol being analyzed, to remove market-wide trends.
        """
        assert len(event_dates) > 0, "event_dates must contain at least one date"
        assert all(isinstance(event_date, date) for event_date in event_dates), "event_dates must contain only date objects"
        assert pre_event >= 0, "pre_event must be a non-negative integer"
        assert post_event >= 0, "post_event must be a non-negative integer"
        assert max_offset >= 0, "max_offset must be a non-negative integer"
        assert benchmark_symbol != symbol, "benchmark_symbol must be different from symbol"
        
        self.symbol = symbol
        self.event_dates = sorted(event_dates, reverse=True)
        self.pre_event = pre_event
        self.post_event = post_event
        self.max_offset = max_offset
        self.start = min(event_dates) - timedelta(days=(pre_event + max_offset) * 1.6)
        self.end = max(event_dates) + timedelta(days=(post_event + max_offset) * 1.6)

        assert self.end <= date.today(), "end date must be in the past, note that buffers are added to the start and end dates"

        self._fetch_data()
        self._generate_initial_tensors()

        if benchmark_symbol:
            self._initialise_benchmark(benchmark_symbol)
            self.benchmarked_delta_tensor = self.delta_tensor - self.benchmark_se.delta_tensor

    def _initialise_benchmark(self, benchmark_symbol: str):
        self.benchmark_se = SymbolEvent(benchmark_symbol, self.event_dates, self.pre_event, self.post_event, self.max_offset, None)

    def _fetch_data(self):
        self.csv_filepath, csv_exists = utils.data_filepath(self.symbol, self.start, self.end, "csv")
        if not csv_exists:
            data_fetch.time_series_to_csv(self.symbol, self.start, self.end)
        
    def _generate_initial_tensors(self):
        self.raw_df = data_analysis.raw_df(self.csv_filepath)
        self.raw_tensor = data_analysis.raw_tensor(self.raw_df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
        self.delta_tensor = data_analysis.delta_tensor(self.raw_tensor)

    def min_mse(self):
        return data_analysis.min_mse(self.delta_tensor, self.max_offset)
