from requests import get
from json import loads
from datetime import date, datetime
from logging import getLogger

logger = getLogger()


class TwelveData:
    _api_endpoint: str = "https://api.twelvedata.com"

    def __init__(self, apikey) -> None:
        self._apikey = apikey

    def _request(self, path: str, params: dict[str, str]) -> str:
        logger.info(f"Params (excluding apikey): {params}")
        params.update({"apikey": self._apikey})
        response = get(f"{TwelveData._api_endpoint}{path}", params)
        if response.status_code != 200:
            logger.error(f"Request failed - {response.status_code}: {response.text}")
            exit(1)
        return response.text
    
    def earliest_timestamp(self, symbol: str) ->  date:
        response = self._request("/earliest_timestamp", {"symbol": symbol, "interval": "1day"})
        print(response)
        return datetime.strptime(loads(response)["datetime"], "%Y-%m-%d").date()

    def time_series(self, symbol: str, start_date: date, end_date: date, **kwargs) -> str:
        params = {
            "symbol": symbol,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "interval": "1day",
            "format": "CSV"
        }
        params.update(kwargs)
        return self._request("/time_series", params)

    def beta(self, symbol: str, start_date: date, end_date: date, **kwargs) -> str:
        params = {
            "symbol": symbol,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "interval": "1day",
            "format": "CSV"
        }
        params.update(kwargs)
        return self._request("/beta", params)

    def stocks(self) -> str:
        return self._request("/stocks", {"format": "CSV"})