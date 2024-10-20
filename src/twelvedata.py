from requests import Response
from datetime import date

class TwelveData:
    _api_endpoint = "https://api.twelvedata.com"

    def __init__(self, apikey) -> None:
        self._apikey = apikey
        self._session = requests.Session()
        self._session.headers.update({"Authorization": self._apikey})

    def _request(self, path: str, params: dict[str, str]) -> str:
        response = self._session.get(f"{TwelveData._api_endpoint}{path}", params)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")
        
        return response.text
    
    def get_time_series(self, symbol: str, start_date: date, end_date: date, interval: str = "1day", **kwargs) -> str:
        assert interval in ("1min", "5min", "15min", "30min", "45min", "1h", "2h", "4h", "1day", "1week", "1month",)
        
        params = {
            symbol: symbol,
            start_date: start_date.strftime("%Y-%m-%d"),
            end_date: end_date.strftime("%Y-%m-%d"),
            interval: interval,
        }
        params.update(kwargs)

        return self._request("/time_series", params)
