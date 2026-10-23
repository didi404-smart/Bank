import json
from datetime import date, datetime
from pathlib import Path

from src.api_clients import get_currency_rates, get_prices
from src.config import load_user_settings
from src.reports import report_cashflow, report_category
from src.utils import read_operations
from src.views import events_page, main_page

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def date_optim(operations: list[dict]) -> datetime:
    """Возвращает текущую дату,  Если за текущий месяц операций нет - возвращает дату последней операции из данных"""
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_ops = [op for op in operations if month_start <= op["operation_datetime"] <= now]
    if month_ops:
        return now
    last_date = max(op["operation_datetime"] for op in operations)
    return last_date


def month_period(dt) -> tuple[date, date]:
    """Возвращает start, end для выбранной даты"""
    d = dt.date() if hasattr(dt, "date") else dt
    return d.replace(day=1), d


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

    start, end = month_period(date_act)
    reports_json = {
        "cashflow": report_cashflow(operations, start=start, end=end),
        "by_category": report_category(operations, start=start, end=end),
    }
    result = {
        "main": main_json,
        "events": events_json,
        "reports": reports_json,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
