from os import path
from datetime import date, timedelta

def get_filename(symbol: str, event_dates: list[date], pre_event: int, post_event: int) -> str:
    start = min(event_dates) - timedelta(days=pre_event)
    end = max(event_dates) + timedelta(days=post_event)
    filename = f"{symbol} {start.strftime('%Y-%m-%d')} {end.strftime('%Y-%m-%d')}.csv"
    return filename

def get_dir(dir: str) -> str:
    return path.join(path.dirname(path.dirname(__file__)), dir)
