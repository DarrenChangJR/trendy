from datetime import date, timedelta
from logging import getLogger

import utils
import data_fetch
import data_analysis
import data_visualisation


class SymbolEvent:
    _benchmark_cache = {}
    logger = getLogger()

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

        # setting & calculating data specific to the 2 datasets
        if self.benchmark_symbol not in SymbolEvent._benchmark_cache:
            SymbolEvent._benchmark_cache[self.benchmark_symbol] = data_fetch.generate_df(self.benchmark_symbol, self.event_dates, self.post_event)
        self.benchmark_df = SymbolEvent._benchmark_cache[self.benchmark_symbol]
        self.df = data_fetch.generate_df(self.symbol, self.event_dates, self.post_event)
        self.df = data_analysis.alpha(self.df, self.benchmark_df)
        self._earliest_alpha = max(self.df.iloc[0].name.date(), self.benchmark_df.iloc[0].name.date())
        self._latest_alpha = min(self.df.iloc[-1].name.date(), self.benchmark_df.iloc[-1].name.date())

        # calculating MSE of principal and random mean squared error losses
        # confidence range: (-infinity, 1]
        random_dates = list(utils.random_dates(
            self._earliest_alpha + timedelta(days=(self.pre_event + self.max_offset) * 2),
            self._latest_alpha - timedelta(days=(self.post_event + self.max_offset) * 2),
            500
        ))
        self.min_mse_random = data_analysis.min_mse(self.df, self.event_dates[0], random_dates, self.pre_event, self.post_event, self.max_offset)
        self.min_mse_random_mean = self.min_mse_random["mse"].mean()
        self.min_mse = data_analysis.min_mse(self.df, self.event_dates[0], self.event_dates[1:], self.pre_event, self.post_event, self.max_offset)
        self.min_mse["confidence"] = (self.min_mse_random_mean - self.min_mse["mse"]) / self.min_mse_random_mean
        
        data_visualisation.main_plot(self.df)