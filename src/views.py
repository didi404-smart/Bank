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
    start = dt.replace(day=1, hour=1, minute=0, second=0, microsecond=0)
    res = []
    for op in operations:
        op_dt = op["operation_datetime"]
        if start <= op_dt <= dt: res.append(op)
    return res