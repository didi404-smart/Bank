from datetime import date, datetime
from collections import defaultdict


def format_date(value) -> date | None:
    """Нормализует значение к date"""
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            return None
    return None


def is_period(op_date: date | None, start: date | None, end: date | None) -> bool:
    """Провиряет находится ли дата в заданном промежутке"""
    if op_date is None:
        return False
    if start is not None and op_date < start:
        return False
    if end is not None and op_date > end:
        return False
    return True


def sum_amount(op: dict) -> float:
    """Достаёт сумму операции"""
    for key in ("amount", "operation_amount", "sum", "payment_amount"):
        if key in op and op[key] is not None:
            try:
                return float(op[key])
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def report_category(
    operations: list[dict], start: date | None = None, end: date | None = None, include_income: bool = False
) -> dict:
    """Отчёт: суммы по категориям за период"""
    totals = defaultdict(float)
    for op in operations:
        op_date = format_date(op.get("operation_datetime") or op.get("date"))
        if not is_period(op_date, start, end):
            continue
        cat = str(op.get("category"))
        amt = sum_amount(op)
        if include_income:
            totals[cat] += amt
        else:
            if amt < 0:
                totals[cat] += abs(amt)
    sort_total = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return {
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
        "include_income": include_income,
        "by_category": [{"category": k, "amount": round(v, 2)} for k, v in sort_total],
    }

def report_cashflow(
        operations: list[dict],
        start: date | None = None,
        end: date | None = None,
) -> dict:
    """ Отчёт: общий кэшфлоу за период"""
    income = 0.0
    expenses = 0.0
    for op in operations:
        op_date = format_date(op.get("operation_datetime") or op.get("date"))
        if not is_period(op_date, start, end):
            continue
        amt = sum_amount(op)
        if amt >= 0:
            income += amt
        else:
            expenses += abs(amt)
    return {
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "net": round(income - expenses, 2),
    }