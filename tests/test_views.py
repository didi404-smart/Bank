from datetime import datetime
import pytest
from src.views import (
    cards_info,
    filter_month_date,
    get_hello,
    main_page,
    parse_datetime,
    top_transactions,
    get_period,
    filter_range,
    events_page,
    top_cashback_cat,
)


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
    operations = operations = [
        {
            "operation_datetime": datetime(2021, 12, 1, 10, 0, 0),
            "card_last4": "1111",
            "amount": -50,
            "category": "A",
            "description": "d1",
            "cashback": 5,
        },
        {
            "operation_datetime": datetime(2021, 12, 2, 10, 0, 0),
            "card_last4": "1111",
            "amount": -10,
            "category": "B",
            "description": "d2",
            "cashback": 2,
        },
        {
            "operation_datetime": datetime(2021, 12, 3, 10, 0, 0),
            "card_last4": "2222",
            "amount": -20,
            "category": "C",
            "description": "d3",
            "cashback": 3,
        },
    ]
    res = main_page("2021-12-31 16:44:00", operations)
    assert set(res.keys()) == {
        "greeting",
        "cards",
        "top_transactions",
        "currency_rates",
        "stock_prices",
        "top_cashback_categories",
    }
    assert res["greeting"] == "Добрый день"
    assert len(res["top_transactions"]) == 3
    assert res["currency_rates"] == []
    assert res["stock_prices"] == []
    assert res["top_cashback_categories"] == [
        {"category": "A", "cashback": 5.0},
        {"category": "C", "cashback": 3.0},
        {"category": "B", "cashback": 2.0},
    ]


def test_get_period():
    dt = datetime(2021, 12, 31, 16, 44, 0)
    start, end = get_period(dt, "M")
    assert start == datetime(2021, 12, 1, 0, 0, 0)
    assert end == dt

    start, end = get_period(dt, "Y")
    assert start == datetime(2021, 1, 1, 0, 0, 0)
    assert end == dt

    start, end = get_period(dt, "W")
    assert start == datetime(2021, 12, 27, 0, 0, 0)
    assert end == dt

    start, end = get_period(dt, "ALL")
    assert end == dt
    assert start <= datetime(1900, 1, 1)

    with pytest.raises(ValueError):
        get_period(dt, "Q")


def test_filter_range():
    start = datetime(2021, 12, 1, 0, 0, 0)
    end = datetime(2021, 12, 31, 23, 59, 59)
    op = [
        {"operation_datetime": datetime(2021, 11, 30, 23, 59, 59), "id": "before"},
        {"operation_datetime": start, "id": "start"},
        {"operation_datetime": datetime(2021, 12, 15, 12, 0, 0), "id": "mid"},
        {"operation_datetime": end, "id": "end"},
        {"operation_datetime": datetime(2022, 1, 1, 0, 0, 0), "id": "after"},
    ]
    res = filter_range(op, start, end)
    assert res == [
        {"operation_datetime": start, "id": "start"},
        {"operation_datetime": datetime(2021, 12, 15, 12, 0, 0), "id": "mid"},
        {"operation_datetime": end, "id": "end"},
    ]


def test_event_page():
    dt = datetime(2021, 12, 20, 10, 0, 0)
    ops = []
    for i in range(8):
        ops.append(
            {
                "operation_datetime": dt,
                "amount": -(10 + i),
                "category": f"Cat{i}",
            }
        )
    result = events_page("2021-12-20 10:00:00", ops, period="M")
    main = result["expenses"]["main"]
    assert len(main) == 8
    assert main[-1]["category"] == "Остальное"
    assert isinstance(main[-1]["amount"], int)

    ops = [
        {"operation_datetime": datetime(2021, 12, 10, 10, 0, 0), "amount": -500, "category": "Переводы"},
        {"operation_datetime": datetime(2021, 12, 10, 10, 0, 0), "amount": -200, "category": "Наличные"},
        {"operation_datetime": datetime(2021, 12, 10, 10, 0, 0), "amount": -100, "category": "Супермаркеты"},
        {"operation_datetime": datetime(2021, 12, 10, 10, 0, 0), "amount": 1000, "category": "Пополнения"},
    ]
    result = events_page("2021-12-31 10:00:00", ops, period="M")
    assert result["expenses"]["cash_and_transfers"] == [
        {"category": "Переводы", "amount": 500},
        {"category": "Наличные", "amount": 200},
    ]
    assert result["incomes"]["total"] == 1000


def test_top_cashback_category():
    ops = [
        {"category": "A", "cashback": 10},
        {"category": "B", "cashback": 5},
        {"category": "C", "cashback": 20},
        {"category": "A", "cashback": 1},
        {"category": "D", "cashback": 7},
    ]
    res = top_cashback_cat(ops)
    assert res == [
        {"category": "C", "cashback": 20.0},
        {"category": "A", "cashback": 11.0},
        {"category": "D", "cashback": 7.0},
    ]
