from datetime import date

from symbol_event import SymbolEvent
from logging_config import setup_logging

def main():
    setup_logging()

    summer_olympics_dates = [
        date(2024, 7, 26),
        date(2021, 7, 23),
        date(2016, 8, 5),
        date(2012, 7, 27),
        date(2008, 8, 8),
        date(2004, 8, 13),
    ]
    pre_event = 4 * 12
    post_event = 10 * 3
    max_offset = 2

    aapl = SymbolEvent("AAPL", summer_olympics_dates, pre_event, post_event, max_offset, "SPLG")
    # aapl.plot_tensors()
    

# if __name__ == "main":
main()