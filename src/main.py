import json
from datetime import datetime
from pathlib import Path

from src.config import load_user_settings
from src.api_clients import get_currency_rates, get_prices
from src.utils import read_operations
from src.views import events_page, main_page

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def date_optim(operations: list[dict]) -> str:
    """Возвращает текущую дату,  Если за текущий месяц операций нет - возвращает дату последней операции из данных"""
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_ops = [op for op in operations if month_start <= op["operation_datetime"] <= now]
    if month_ops:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    last_date = max(op["operation_datetime"] for op in operations)
    return last_date.strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    operations_path = PROJECT_ROOT / "data" / "operations.xlsx"
    settings_path = PROJECT_ROOT / "user_settings.json"
    operations = read_operations(str(operations_path))
    settings = load_user_settings(str(settings_path))

    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    date_act = date_optim(operations)

    currency_rates = get_currency_rates(currencies)
    stock_prices = get_prices(stocks)

    main_json = main_page(date_act, operations, currency_rates, stock_prices)
    events_json = events_page(date_act, operations, currency_rates, stock_prices)

    print("Дата/время запроса:", date_act)
    print("\nMAIN PAGE JSON:")
    print(json.dumps(main_json, ensure_ascii=False, indent=2))
    print("\nEVENTS PAGE JSON:")
    print(json.dumps(events_json, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
