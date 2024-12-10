from datetime import date, timedelta
from logging import getLogger

import utils
import data_fetch
import data_analysis
import data_visualisation


class SymbolEvent:
    _benchmark_cache = {}
    logger = getLogger()

    def __init__(self, symbol: str, event_dates: list[date], pre_event: int, post_event: int, max_offset: int, benchmark_symbol: str = "SPY") -> None:
        """
        Args:
            symbol (str): The symbol of the stock to analyze.
            event_dates (list[date]): The dates of the events to analyze.
            pre_event (int): The number of days before the event to include in trend analysis.
            post_event (int): The number of days after the event to include in trend analysis.
            max_offset (int): The maximum number of days to offset the event date by, used by event dates other than the latest one.
            benchmark_symbol (str, optional): The symbol to subtract from the symbol being analyzed, to remove market-wide trends. Defaults to "SPY".
        """
        assert len(event_dates) > 0, "event_dates must contain at least one date"
        assert all(isinstance(event_date, date) for event_date in event_dates), "event_dates must contain only date objects"
        assert pre_event >= 0, "pre_event must be a non-negative integer"
        assert post_event >= 0, "post_event must be a non-negative integer"
        assert max_offset >= 0, "max_offset must be a non-negative integer"
        assert benchmark_symbol != symbol, "benchmark_symbol must be different from symbol"
        
        event_dates.sort(reverse=True)

        # fetch the benchmark data, cache since benchmark is likely the same across instances
        if benchmark_symbol not in SymbolEvent._benchmark_cache:
            SymbolEvent._benchmark_cache[benchmark_symbol] = data_fetch.generate_df(benchmark_symbol, event_dates, post_event)
        self.benchmark_df = SymbolEvent._benchmark_cache[benchmark_symbol]
        
        # fetch the symbol data
        self.df = data_fetch.generate_df(symbol, event_dates, post_event)

        # calculate the alpha (excess return) and minimum mean squared error (MSE)
        self.df = data_analysis.alpha(self.df, self.benchmark_df)
        self.min_mse = data_analysis.min_mse(self.df, event_dates[0], event_dates[1:], pre_event, post_event, max_offset)
        

        # sample random dates for comparison
        _earliest_random_date = max(self.df.iloc[0].name.date(), self.benchmark_df.iloc[0].name.date()) + timedelta(days=(pre_event + max_offset) * 2)
        _latest_random_date = min(self.df.iloc[-1].name.date(), self.benchmark_df.iloc[-1].name.date()) - timedelta(days=(post_event + max_offset) * 2)
        random_dates = list(utils.random_dates(_earliest_random_date, _latest_random_date, 500))
        min_mse_random = data_analysis.min_mse(self.df, event_dates[0], random_dates, pre_event, post_event, max_offset)


        # log the results
        # SymbolEvent.logger.info(f"Symbol: {symbol}")
        # SymbolEvent.logger.info(self.min_mse)
        print(self.min_mse)
        print(min_mse_random.head())
        print(min_mse_random["mse"].mean())
        # either form a 5% confidence interval around the mean then count how many events fall outside of it, which means they are significant
        # or just print all the p-values
        
        data_visualisation.main_plot(self.df, event_dates)