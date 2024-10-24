from datetime import date
import logging

from symbol_event import SymbolEvent
from logging_config import setup_logging

def main():
    setup_logging()
    logger = logging.getLogger()

    summer_olympics_dates = [
        date(2024, 7, 26),
        date(2021, 7, 23),
        date(2016, 8, 5),
        date(2012, 7, 27),
        date(2008, 8, 8),
        date(2004, 8, 13),
    ]
    aapl = SymbolEvent("AAPL", summer_olympics_dates, 4 * 12, 10 * 3, 10)
    aapl.min_mse()

# if __name__ == "main":
main()