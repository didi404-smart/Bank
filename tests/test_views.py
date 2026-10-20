from datetime import datetime

from src.views import filter_month_date, get_hello, parse_datetime


def test_get_hello():
    assert get_hello(datetime(2026, 1, 1, 6, 0, 0)) == "Доброе утро"
    assert get_hello(datetime(2026, 1, 1, 12, 0, 0)) == "Добрый день"
    assert get_hello(datetime(2026, 1, 1, 18, 0, 0)) == "Добрый вечер"
    assert get_hello(datetime(2026, 1, 1, 23, 0, 0)) == "Доброй ночи"


def test_parse_datetime():
    assert parse_datetime("2021-12-31 16:44:00") == datetime(2021, 12, 31, 16, 44, 0)


def test_filter_month_date():
    start = datetime(2021, 12, 1, 0, 0, 0)
    dt = datetime(2021, 12, 31, 16, 44, 0)
    operations = [
        {"operation_datetime": datetime(2021, 11, 30, 23, 59, 59)},
        {"operation_datetime": start},
        {"operation_datetime": datetime(2021, 12, 15, 12, 0, 0)},
        {"operation_datetime": dt},
        {"operation_datetime": datetime(2021, 12, 31, 16, 44, 1)},
    ]
    res = filter_month_date(operations, dt)
    res_dt = [op["operation_datetime"] for op in res]
    assert res_dt == [
        start,
        datetime(2021, 12, 15, 12, 0, 0),
        dt,
    ]
