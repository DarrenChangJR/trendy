from datetime import date
import data_fetch

data_fetch.time_series_to_csv("AAPL", date(1900, 1, 1), date(2021, 1, 1))