from datetime import datetime, time
from collections import defaultdict


def parse_datetime(date_time: str) -> datetime:
    """Преобразует входную строку даты/времени формата 'YYYY-MM-DD HH:MM:SS' в datetime."""
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")


def get_hello(dt: datetime) -> str:
    """Возвращает приветствие в зависимости от времени"""
    t = dt.time()
    if time(6, 0) <= t <= time(11, 59, 59):
        return "Доброе утро"
    if time(12, 0) <= t <= time(17, 59, 59):
        return "Добрый день"
    if time(18, 0) <= t <= time(22, 59, 59):
        return "Добрый вечер"
    return "Доброй ночи"


def filter_month_date(operations: list[dict], dt: datetime) -> list[dict]:
    """Возвращает операции в диапазоне: с 1-го числа месяца (00:00:00) по dt включительно."""
    start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    res = []
    for op in operations:
        op_dt = op["operation_datetime"]
        if start <= op_dt <= dt:
            res.append(op)
    return res


def format_date(dt: datetime) -> str:
    """Форматирует datetime в строку 'dd.mm.yyyy"""
    return dt.strftime("%d.%m.%Y")


def top_transactions(operations: list[dict], limit: int = 5) -> list[dict]:
    """Возвращает top транзакций, отсортированных по убыванию amount."""
    sort_ops = sorted(operations, key=lambda op: float(op.get("amount", 0)), reverse=True)
    top_ops = sort_ops[:limit]
    res = []
    for op in top_ops:
        res.append(
            {
                "date": format_date(op["operation_datetime"]),
                "amount": float(op.get("amount", 0)),
                "category": op.get("category", ""),
                "description": op.get("description", ""),
            }
        )
    return res


def cards_info(operations: list[dict]) -> list[dict]:
    """Формирует информацию по картам: последние 4 цифры, сумма расходов по карте, 1 рубль на каждые 100 рублей расходов"""
    spent_card = defaultdict(float)
    for op in operations:
        card = op.get("card_last4")
        if not card:
            continue
        amount = float(op.get("amount", 0))
        if amount < 0:
            spent_card[card] += abs(amount)
    cards = []
    for last4, total_spent in spent_card.items():
        cards.append(
            {"last_digits": last4, "total_spent": round(total_spent, 2), "cashback": int(total_spent // 100)}
        )
    cards.sort(key=lambda x: x["last_digits"])
    return cards

def main_page(date_time: str, operations: list[dict]) -> dict:
    """Формирует JSON-данные для страницы «Главная» за период с начала месяца по указанную дату."""
    dt = parse_datetime(date_time)
    month_ops = filter_month_date(operations, dt)
    return {
        "greeting": get_hello(dt),
        "cards": cards_info(month_ops),
        "top_transactions": top_transactions(month_ops, limit=5),
        "currency_rates": [],
        "stock_prices": [],
    }