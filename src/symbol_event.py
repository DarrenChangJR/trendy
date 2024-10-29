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

        self.df = data_fetch.generate_df(self.symbol, self.event_dates, self.post_event, self.max_offset)
        
        if self.benchmark_symbol not in SymbolEvent._benchmark_cache:
            SymbolEvent._benchmark_cache[self.benchmark_symbol] = data_fetch.generate_df(self.benchmark_symbol, self.event_dates, self.post_event, self.max_offset)
        self.benchmark_df = SymbolEvent._benchmark_cache[self.benchmark_symbol]

        self.df = data_analysis.add_alpha(self.df, self.benchmark_df)
        self.min_mse = data_analysis.min_mse(self.df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
        random_dates = utils.random_dates(self.df.iloc[0].name.date())
        # self._correlate()

    # def _generate_df(self) -> None:
    #     pass
        # self.csv_filepath, csv_exists = utils.data_filepath(self.symbol, self.start, self.end, "csv")
        # if not csv_exists:
        #     data_fetch.time_series_to_csv(self.symbol, self.start, self.end)
        
        # benchmark_csv_filepath, benchmark_csv_exists = utils.data_filepath(self.benchmark_symbol, self.start, self.end, "csv")
        # if not benchmark_csv_exists:
        #     data_fetch.time_series_to_csv(self.benchmark_symbol, self.start, self.end)
        
        # self.df = data_analysis.df(self.csv_filepath, benchmark_csv_filepath)

    def _correlate(self) -> None:
        pass
        # self.alpha_loss = data_analysis.min_mse(self.df, self.event_dates, self.pre_event, self.post_event, self.max_offset)
        
        # random_dates = [self.event_dates[0]] + list(utils.random_dates(self.start, self.end, 100))
        # self.avg_random_loss = data_analysis.min_mse(self.df, random_dates, self.pre_event, self.post_event, self.max_offset)["mse"].mean()
