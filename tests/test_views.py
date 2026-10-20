from datetime import datetime

from src.views import filter_month_date, get_hello, parse_datetime, top_transactions, cards_info, main_page


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

def test_cards_info():
    operations = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0, 0), "card_last4": "1111", "amount": -50},
        {"operation_datetime": datetime(2021, 12, 2, 10, 0, 0), "card_last4": "1111", "amount": -60},
        {"operation_datetime": datetime(2021, 12, 3, 10, 0, 0), "card_last4": "1111", "amount": 1000},
        {"operation_datetime": datetime(2021, 12, 1, 10, 0, 0), "card_last4": "2222", "amount": -250},
        {"operation_datetime": datetime(2021, 12, 1, 10, 0, 0), "card_last4": None, "amount": -999},
    ]
    res = cards_info(operations)
    assert res == [
        {"last_digits": "1111", "total_spent": 110.0, "cashback": 1},
        {"last_digits": "2222", "total_spent": 250.0, "cashback": 2},
    ]

def test_main_page():
    operations = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0, 0), "card_last4": "1111", "amount": -50,
         "category": "A", "description": "d1"}
    ]
    res = main_page("2021-12-31 16:44:00", operations)
    assert set(res.keys()) == {"greeting", "cards", "top_transactions", "currency_rates", "stock_prices"}
    assert res["greeting"] == "Добрый день"
    assert len(res["top_transactions"]) == 1
    assert res["currency_rates"] == []
    assert res["stock_prices"] == []