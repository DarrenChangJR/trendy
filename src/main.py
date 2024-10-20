from data_analysis import SymbolEvent
from datetime import date
    

def main() -> None:
    symbol_event = SymbolEvent("AAPL", [date.today()], 5, 5)
    # print(symbol_event.tensor)

# if __name__ == "main":
main()