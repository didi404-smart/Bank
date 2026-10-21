from collections import defaultdict
from datetime import datetime, time, timedelta

CASH_AND_TRANSFERS = {"Переводы", "Наличные"}


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
        cards.append({"last_digits": last4, "total_spent": round(total_spent, 2), "cashback": int(total_spent // 100)})
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


def get_period(dt: datetime, period: str = "M") -> tuple[datetime, datetime]:
    """Возвращает (start, end) для выбранного периода"""
    period = period.upper()
    end = dt
    if period == "M":
        start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, end
    if period == "Y":
        start = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, end
    if period == "W":
        start = (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, end
    if period == "ALL":
        start = datetime.min.replace(hour=0, minute=0, second=0, microsecond=0)
        return start, end
    raise ValueError("period must be one of: W, M, Y, ALL")


def filter_range(operations: list[dict], start: datetime, end: datetime) -> list[dict]:
    """Возвращает операции, у которых start <= operation_datetime <= end"""
    res = []
    for op in operations:
        op_dt = op["operation_datetime"]
        if start <= op_dt <= end:
            res.append(op)
    return res


def events_page(date_time: str, operations: list[dict], period: str = "M") -> dict:
    """Формирует JSON-данные для страницы 'События'"""
    dt = parse_datetime(date_time)
    start, end = get_period(dt, period)
    ops = filter_range(operations, start, end)
    expense_ops = [op for op in ops if float(op.get("amount", 0)) < 0]
    income_ops = [op for op in ops if float(op.get("amount", 0)) > 0]
    expense_cat = defaultdict(float)
    income_cat = defaultdict(float)
    for op in expense_ops:
        cat = op.get("category", "")
        expense_cat[cat] += abs(float(op.get("amount", 0)))
    for op in income_ops:
        cat = op.get("category", "")
        income_cat[cat] += float(op.get("amount", 0))
    total_expenses = sum(expense_cat.values())
    total_incomes = sum(income_cat.values())
    sorted_exp = sorted(expense_cat.items(), key=lambda x: x[1], reverse=True)
    top_7 = sorted_exp[:7]
    rest = sorted_exp[7:]
    rest_sum = sum(amount for cat, amount in rest)
    expenses = [{"category": cat, "amount": int(round(amount))} for cat, amount in top_7]
    if rest_sum > 0:
        expenses.append({"category": "Остальное", "amount": int(round(rest_sum))})
    cash_transfers = []
    for cat in CASH_AND_TRANSFERS:
        if cat in expense_cat:
            cash_transfers.append((cat, expense_cat[cat]))
    cash_transfers.sort(key=lambda x: x[1], reverse=True)
    expenses_cash = [{"category": cat, "amount": int(round(amount))} for cat, amount in cash_transfers]

    sorted_income = sorted(income_cat.items(), key=lambda x: x[1], reverse=True)
    incomes = [{"category": cat, "amount": int(round(amount))} for cat, amount in sorted_income]
    return {
        "expenses": {
            "total": int(round(total_expenses)),
            "main": expenses,
            "cash_and_transfers": expenses_cash,
        },
        "incomes": {
            "total": int(round(total_incomes)),
            "main": incomes,
        },
        "currency_rates": [],
        "stock_prices": [],
    }

def top_cashback_cat(operations: list[dict], limit: int = 3) -> list[dict]:
    """Возвращает топ категорий по суммарному кешбэку"""
    cashback_cat = defaultdict(float)
    for op in operations:
        cat = op.get("category", "")
        cashback = float(op.get("cashback", 0))
        cashback_cat[cat] += cashback
    sorted_cashback = sorted(cashback_cat.items(), key=lambda  x: x[1], reverse=True)
    top = sorted_cashback[:limit]
    return [{"category": cat, "cashback": cash} for cat, cash in top]