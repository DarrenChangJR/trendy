from os import path
from datetime import date, timedelta
from random import random

def file_path(file: str) -> tuple[str, bool]:
    filepath = path.join(path.dirname(path.dirname(__file__)), file)
    return filepath, path.exists(filepath)

def random_dates(start: date, end: date, n: int) -> set[date]:
    possible_days = (end - start).days
    return {start + timedelta(days=random() * possible_days) for _ in range(n)}
