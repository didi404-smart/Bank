from datetime import datetime

from src.views import filter_month_date, get_hello, parse_datetime, top_transactions


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

def test_top_transactions():
    ops = [
        {"operation_datetime": datetime(2021, 12, 30, 10, 0, 0), "amount": -100, "category": "A", "description": "d1"},
        {"operation_datetime": datetime(2021, 12, 30, 10, 0, 0), "amount": 50, "category": "B", "description": "d2"},
        {"operation_datetime": datetime(2021, 12, 30, 10, 0, 0), "amount": 10, "category": "C", "description": "d3"},
        {"operation_datetime": datetime(2021, 12, 30, 10, 0, 0), "amount": 999, "category": "D", "description": "d4"},
        {"operation_datetime": datetime(2021, 12, 30, 10, 0, 0), "amount": 0, "category": "E", "description": "d5"},
        {"operation_datetime": datetime(2021, 12, 30, 10, 0, 0), "amount": 5, "category": "F", "description": "d6"},
    ]
    res = top_transactions(ops)
    assert len(res) == 5
    assert [x["amount"] for x in res] == [999.0, 50.0, 10.0, 5.0, 0.0]
    for item in res:
        assert set(item.keys()) == {"date", "amount", "category", "description"}
        assert item["date"] == "30.12.2021"