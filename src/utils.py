from os import path
from datetime import date

def data_filepath(symbol: str, start: date, end: date, extension: str) -> tuple[str, bool]:
    data_dir = path.join(path.dirname(path.dirname(__file__)), "data")
    filename = f"{symbol} {start.strftime('%Y-%m-%d')} {end.strftime('%Y-%m-%d')}.{extension}"
    filepath = path.join(data_dir, filename)
    return filepath, path.exists(filepath)
