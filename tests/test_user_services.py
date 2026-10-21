from datetime import datetime

from src.user_services import format_phone, search_description, search_phone


def test_search_description():
    ops = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0), "description": "Колхоз"},
        {"operation_datetime": datetime(2021, 12, 2, 10, 0), "description": "Ozon.ru"},
        {"operation_datetime": datetime(2021, 12, 3, 10, 0), "description": "Магнит"},
    ]
    assert search_description(ops, "кол") == [ops[0]]


def test_format_phone():
    assert format_phone("+7 (900) 000-00-00") == "79000000000"
    assert format_phone("8 900 000-00-00") == "79000000000"
    assert format_phone("9000000000") == "79000000000"
    assert format_phone("12345") == ""


def test_search_phone():
    ops = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0), "description": "Перевод +7 (900) 000-00-00"},
        {"operation_datetime": datetime(2021, 12, 2, 10, 0), "description": "Перевод 89000000000"},
        {"operation_datetime": datetime(2021, 12, 3, 10, 0), "description": "Покупка в магазине"},
    ]
    res = search_phone(ops, "8 (900) 000-00-00")
    assert res == [ops[0], ops[1]]

    assert search_phone(ops, "not phone") == []
