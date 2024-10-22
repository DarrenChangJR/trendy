from symbol_event import SymbolEvent
from datetime import date
    

def main():
    # get data
    summer_olympics_dates = [
        date(2024, 7, 26),
        date(2021, 7, 23),
        date(2016, 8, 5),
        date(2012, 7, 27),
        date(2008, 8, 8),
        date(2004, 8, 13),
    ]
    aapl = SymbolEvent("AAPL", summer_olympics_dates, 5 * 12, 10 * 8, 10)

# if __name__ == "main":
main()