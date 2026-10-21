from unittest.mock import Mock, patch

import pytest
from requests import RequestException

from src.api_clients import get_currency_rates, get_prices


@patch("src.api_clients.API_KEY", "test_api_key")
@patch("src.api_clients.requests.get")
def test_get_currency(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Realtime Currency Exchange Rate": {"5. Exchange Rate": "0.0124"}}
    mock_get.return_value = mock_response
    res = get_currency_rates(["USD"])
    assert res == [{"currency": "USD", "rate": 0.0124}]
    args, kwargs = mock_get.call_args
    assert kwargs["params"]["function"] == "CURRENCY_EXCHANGE_RATE"
    assert kwargs["params"]["from_currency"] == "RUB"
    assert kwargs["params"]["to_currency"] == "USD"
    assert kwargs["params"]["apikey"] == "test_api_key"


@patch("src.api_clients.API_KEY", "test_api_key")
@patch("src.api_clients.requests.get")
def test_get_currency_zero(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Realtime Currency Exchange Rate": {"5. Exchange Rate": "0"}}
    mock_get.return_value = mock_response
    res = get_currency_rates(["USD"])
    assert res == [{"currency": "USD", "rate": 1.0}]


@patch("src.api_clients.API_KEY", "test_api_key")
@patch("src.api_clients.requests.get")
def test_get_currency_error(mock_get):
    mock_get.side_effect = RequestException("error")
    res = get_currency_rates(["USD", "EUR"])
    assert res == [
        {"currency": "USD", "rate": 1.0},
        {"currency": "EUR", "rate": 1.0},
    ]


@patch("src.api_clients.API_KEY", "test_api_key")
@patch("src.api_clients.requests.get")
def test_get_prices(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Global Quote": {"05. price": "123.45"}}
    mock_get.return_value = mock_response
    res = get_prices(["AAPL"])
    assert res == [{"stock": "AAPL", "price": 123.45}]
    args, kwargs = mock_get.call_args
    assert kwargs["params"]["function"] == "GLOBAL_QUOTE"
    assert kwargs["params"]["symbol"] == "AAPL"
    assert kwargs["params"]["apikey"] == "test_api_key"


@patch("src.api_clients.API_KEY", "test_api_key")
@patch("src.api_clients.requests.get")
def test_get_prices_zero(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"Global Quote": {"05. price": "0"}}
    mock_get.return_value = mock_response
    res = get_prices(["AAPL"])
    assert res == [{"stock": "AAPL", "price": 1.0}]


@patch("src.api_clients.API_KEY", None)
def test_no_api_key():
    with pytest.raises(RuntimeError):
        get_prices(["AAPL"])

    with pytest.raises(RuntimeError):
        get_currency_rates(["USD"])
