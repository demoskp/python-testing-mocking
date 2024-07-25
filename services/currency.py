import requests


class FXRateServiceException(Exception):
    pass


class FXRateService:
    BASE_URL = "https://api.currencylayer.com"

    def __init__(self, access_key):
        self._response = None
        self._access_key = access_key

    def historical(self, from_fx, to_fx, date):
        params = {"access_key": self._access_key, "source": from_fx, "currencies": to_fx, "date": date}
        self._response = requests.get(self.BASE_URL + "/historical", params=params)
        self._validate_response()
        return self._extract_fx_rate(from_fx, to_fx)

    def current(self, from_fx, to_fx):
        params = {"access_key": self._access_key, "source": from_fx, "currencies": to_fx}
        self._response = requests.get(self.BASE_URL + "/live", params=params)
        self._validate_response()
        return self._extract_fx_rate(from_fx, to_fx)

    def _validate_response(self):
        if self._response.status_code != 200:
            raise FXRateServiceException("Request to fetch fx rate failed")

        data = self._response.json()
        success = data.get("success")

        if not success:
            error_info = data.get('error').get('info')
            raise FXRateServiceException(f"There was an error fetching the fx rate, {error_info}")

        quotes = data.get("quotes")

        if not quotes:
            raise FXRateServiceException("Not fx rate found")

    def _extract_fx_rate(self, from_fx, to_fx):
        data = self._response.json()
        quotes = data.get("quotes")
        return quotes.get(f"{from_fx}{to_fx}")
