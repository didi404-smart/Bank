from datetime import datetime, time


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
    sort_ops = sorted(operations, key=lambda  op: float(op.get("amount", 0)), reverse=True)
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

