from datetime import date, timedelta

import utils
import data_fetch
import data_analysis


class SymbolEvent:
    _benchmark_cache = {}

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
        self.benchmark_symbol = benchmark_symbol
        self.start = self.event_dates[-1] - timedelta(days=(pre_event + max_offset) * 1.6)
        self.end = self.event_dates[0] + timedelta(days=(post_event + max_offset) * 1.6)

        assert self.end <= date.today(), "end date must be in the past, note that buffers are added to the start and end dates"

        self._generate_df()
        self._correlate()
        # self.min_mse = data_analysis.min_mse(self.df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
        # self._generate_raw_tensors()

        # if not benchmark_symbol:
        #     return
        
        # self._benchmark(benchmark_symbol)
        # self._detect_correration()

    def _generate_df(self) -> None:
        self.csv_filepath, csv_exists = utils.data_filepath(self.symbol, self.start, self.end, "csv")
        if not csv_exists:
            data_fetch.time_series_to_csv(self.symbol, self.start, self.end)
        
        benchmark_csv_filepath, benchmark_csv_exists = utils.data_filepath(self.benchmark_symbol, self.start, self.end, "csv")
        if not benchmark_csv_exists:
            data_fetch.time_series_to_csv(self.benchmark_symbol, self.start, self.end)
        
        self.df = data_analysis.df(self.csv_filepath, benchmark_csv_filepath)

    # def _generate_raw_tensors(self) -> None:
    #     self.raw_tensor = data_analysis.raw_tensor(self.raw_df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
    #     self.delta_tensor = data_analysis.delta_tensor(self.raw_tensor)

    # def _benchmark(self, benchmark_symbol: str) -> None:
    #     if benchmark_symbol not in SymbolEvent._benchmark_cache:
    #         SymbolEvent._benchmark_cache[benchmark_symbol] = SymbolEvent(benchmark_symbol, self.event_dates, self.pre_event, self.post_event, self.max_offset, None)
    #     self.benchmark_se = SymbolEvent._benchmark_cache[benchmark_symbol]
    #     self.alpha_tensor = self.delta_tensor - self.benchmark_se.delta_tensor

    def _correlate(self) -> None:
        self.alpha_loss = data_analysis.min_mse(self.df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
        
        random_dates = [self.event_dates[0]] + list(utils.random_dates(self.start, self.end, 100))
        self.avg_random_loss = data_analysis.min_mse(self.df, random_dates, self.pre_event, self.post_event, self.max_offset)["mse"].mean()


    # def min_mse(self):
    #     return data_analysis.min_mse(self.alpha_tensor, self.max_offset)

    # def plot_tensors(self):
    #     data_visualisation.plot_raw_tensor(self.raw_tensor, self.event_dates)
    #     data_visualisation.plot_delta_tensor(self.delta_tensor, self.event_dates)
    #     data_visualisation.plot_alpha_tensor(self.alpha_tensor, self.event_dates)
