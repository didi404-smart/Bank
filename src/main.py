import json
from datetime import datetime
from pathlib import Path

from src.config import load_user_settings
from src.services import get_currency_rates, get_prices
from src.utils import read_operations
from src.views import events_page, main_page

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    operations_path = PROJECT_ROOT / "data" / "operations.xlsx"
    settings_path = PROJECT_ROOT / "user_settings.json"
    operations = read_operations(str(operations_path))
    settings = load_user_settings(str(settings_path))
    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    currency_rates = get_currency_rates(currencies)
    stock_prices = get_prices(stocks)
    main_json = main_page(now_str, operations)
    main_json["currency_rates"] = currency_rates
    main_json["stock_prices"] = stock_prices
    events_json = events_page(now_str, operations)
    events_json["currency_rates"] = currency_rates
    events_json["stock_prices"] = stock_prices

    print("Дата/время запроса:", now_str)
    print("\nMAIN PAGE JSON:")
    print(json.dumps(main_json, ensure_ascii=False, indent=2))
    print("\nEVENTS PAGE JSON:")
    print(json.dumps(events_json, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
