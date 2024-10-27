from os import path
from datetime import date, timedelta
from random import random

def data_filepath(symbol: str, start: date, end: date, extension: str) -> tuple[str, bool]:
    data_dir = path.join(path.dirname(path.dirname(__file__)), "data")
    filename = f"{symbol}_{start.strftime('%Y-%m-%d')}_{end.strftime('%Y-%m-%d')}.{extension}"
    filepath = path.join(data_dir, filename)
    return filepath, path.exists(filepath)

def random_dates(start: date, end: date, n: int) -> set[date]:
    possible_days = (end - start).days
    return {start + timedelta(days=random() * possible_days) for _ in range(n)}
