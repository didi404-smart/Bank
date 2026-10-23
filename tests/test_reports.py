from datetime import date, datetime
from src.reports import report_cashflow, report_category, format_date, is_period, sum_amount

def test_report_category():
    ops = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0), "category": "Еда", "amount": -100},
        {"operation_datetime": datetime(2021, 12, 2, 10, 0), "category": "Еда", "amount": -50},
        {"operation_datetime": datetime(2021, 12, 3, 10, 0), "category": "Зарплата", "amount": 1000},
    ]
    res = report_category(ops)
    assert res["include_income"] is False
    assert res["by_category"] == [{"category": "Еда", "amount": 150.0}]

    ops = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0), "category": "Еда", "amount": -100},
        {"operation_datetime": datetime(2021, 12, 2, 10, 0), "category": "Зарплата", "amount": 1000},
        {"operation_datetime": datetime(2021, 12, 10, 10, 0), "category": "Еда", "amount": -30},
    ]
    res = report_category(ops, start=date(2021, 12, 2), end=date(2021, 12, 9), include_income=True)
    assert res["by_category"] == [{"category": "Зарплата", "amount": 1000.0}]

def test_report_cashflow():
    ops = [
        {"operation_datetime": "2021-12-01 10:00:00", "amount": -200},
        {"operation_datetime": "2021-12-02", "amount": 500},
        {"operation_datetime": None, "amount": 999},
    ]
    res = report_cashflow(ops)
    assert res["income"] == 500.0
    assert res["expenses"] == 200.0
    assert res["net"] == 300.0


def test_format_date():
    assert format_date(None) is None
    assert format_date(date(2021, 12, 1)) == date(2021, 12, 1)
    assert format_date(datetime(2021, 12, 1, 10, 0)) == date(2021, 12, 1)
    assert format_date("2021-12-01 10:00:00") == date(2021, 12, 1)
    assert format_date("not-a-date") is None
    assert format_date(12345) is None

def test_is_period():
    d = date(2021, 12, 5)
    assert is_period(None, None, None) is False
    assert is_period(d, start=date(2021, 12, 6), end=None) is False
    assert is_period(d, start=None, end=date(2021, 12, 4)) is False
    assert is_period(d, start=date(2021, 12, 1), end=date(2021, 12, 31)) is True

def test_sum_amount():
    assert sum_amount({}) == 0.0
    assert sum_amount({"amount": -10}) == -10.0
    assert sum_amount({"amount": "abc"}) == 0.0
    assert sum_amount({"operation_amount": "5"}) == 5.0