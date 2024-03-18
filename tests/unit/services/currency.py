import unittest
from unittest.mock import patch

import pytest

from services.currency import FXRateService, FXRateServiceException


class TestFXRateService(unittest.TestCase):
    fx_response = {
        "success": True,
        "terms": "https://currencylayer.com/terms",
        "privacy": "https://currencylayer.com/privacy",
        "timestamp": 1430401802,
        "source": "USD",
        "quotes": {
            "EUR": 0.90,
            "CAD": 1.40,
            "AUD": 1.50,
        }
    }

    @patch("services.currency.requests.get")
    def test_current_gets_value(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        assert fx_rate_service.current("USD", "EUR") == 0.90
        assert fx_rate_service.current("USD", "CAD") == 1.40
        assert fx_rate_service.current("USD", "AUD") == 1.50

        assert mock_get.call_count == 3

    @patch("services.currency.requests.get")
    def test_historical_gets_value(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"
        assert fx_rate_service.historical("USD", "EUR", date) == 0.90
        assert fx_rate_service.historical("USD", "CAD", date) == 1.40
        assert fx_rate_service.historical("USD", "AUD", date) == 1.50

        assert mock_get.call_count == 3

    @patch("services.currency.requests.get")
    def test_raises_exception_status_not_200(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = self.fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"

        with pytest.raises(FXRateServiceException):
            fx_rate_service.current("USD", "EUR")

        with pytest.raises(FXRateServiceException):
            fx_rate_service.historical("USD", "EUR", date)

    @patch("services.currency.requests.get")
    def test_raises_exception_success_false(self, mock_get):
        mock_get.return_value.status_code = 200
        fx_response = self.fx_response.copy()
        fx_response["success"] = False
        fx_response["error"] = {
            "info": "Some random error"
        }

        mock_get.return_value.json.return_value = fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"

        with pytest.raises(FXRateServiceException):
            fx_rate_service.current("USD", "EUR")

        with pytest.raises(FXRateServiceException):
            fx_rate_service.historical("USD", "EUR", date)

    @patch("services.currency.requests.get")
    def test_raises_exception_no_quotes(self, mock_get):
        mock_get.return_value.status_code = 200
        fx_response = self.fx_response.copy()
        fx_response["success"] = True
        fx_response["quotes"] = {}

        mock_get.return_value.json.return_value = fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"

        with pytest.raises(FXRateServiceException):
            fx_rate_service.current("USD", "EUR")

        with pytest.raises(FXRateServiceException):
            fx_rate_service.historical("USD", "EUR", date)
