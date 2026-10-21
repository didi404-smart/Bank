from datetime import datetime

from src.user_services import search_description

def test_search_description():
    ops = [
        {"operation_datetime": datetime(2021, 12, 1, 10, 0), "description": "Колхоз"},
        {"operation_datetime": datetime(2021, 12, 2, 10, 0), "description": "Ozon.ru"},
        {"operation_datetime": datetime(2021, 12, 3, 10, 0), "description": "Магнит"},
    ]
    assert search_description(ops, "кол") == [ops[0]]