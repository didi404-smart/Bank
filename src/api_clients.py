import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ALPHA_URL = "https://www.alphavantage.co/query"


def get_currency_rates(currencies: list[str], base: str = "RUB") -> list[dict]:
    """Получает курсы валют, Возвращает список словарей"""
    res = []
    if not API_KEY:
        raise RuntimeError("API_KEY not found in environment (.env)")
    for cur in currencies:
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": base,
            "to_currency": cur,
            "apikey": API_KEY,
        }
        try:
            response = requests.get(ALPHA_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            if rate <= 0:
                raise ValueError("rate must be > 0")
            res.append({"currency": cur, "rate": rate})
        except requests.RequestException, KeyError, TypeError, ValueError:
            res.append({"currency": cur, "rate": 1.0})
    return res


def get_prices(stocks: list[str]) -> list[dict]:
    """Получает цены акций"""
    res = []
    if not API_KEY:
        raise RuntimeError("API_KEY not found in environment (.env)")
    for symbol in stocks:
        try:
            params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": API_KEY}
            response = requests.get(ALPHA_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            if price <= 0:
                raise ValueError("price must be > 0")
            res.append({"stock": symbol, "price": price})
        except requests.RequestException, KeyError, TypeError, ValueError:
            res.append({"stock": symbol, "price": 1.0})
    return res
