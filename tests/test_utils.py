from datetime import datetime
from unittest.mock import patch

import pandas as pd

from src.utils import operation_datetime, read_operations


@patch("src.utils.pd.read_excel")
def test_read_operation(mock_read_excel):
    df = pd.DataFrame(
        [
            {
                "Дата операции": "31.12.2021 16:44:00",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма платежа": -160.89,
                "Валюта платежа": "RUB",
                "Категория": "Супермаркеты",
                "Описание": "Колхоз",
                "Кэшбэк": 100,
            }
        ]
    )
    mock_read_excel.return_value = df
    res = read_operations("path.xlsx")
    assert isinstance(res, list)
    assert len(res) == 1
    op = res[0]
    assert op["operation_datetime"] == datetime(2021, 12, 31, 16, 44, 0)
    assert op["card_last4"] == "7197"
    assert op["status"] == "OK"
    assert op["amount"] == -160.89
    assert op["currency"] == "RUB"
    assert op["category"] == "Супермаркеты"
    assert op["description"] == "Колхоз"
    assert op["cashback"] == 100

    mock_read_excel.assert_called_once()


@patch("src.utils.pd.read_excel")
def test_read_operation2(mock_read_excel):
    df = pd.DataFrame(
        [
            {
                "Дата операции": "31.12.2021 16:44:00",
                "Номер карты": "719",
                "Статус": "OK",
                "Сумма платежа": -160.89,
                "Валюта платежа": "RUB",
                "Категория": "Супермаркеты",
                "Описание": "Колхоз",
            }
        ]
    )
    mock_read_excel.return_value = df
    res = read_operations("path.xlsx")
    assert isinstance(res, list)
    assert len(res) == 1
    op = res[0]
    assert op["operation_datetime"] == datetime(2021, 12, 31, 16, 44, 0)
    assert op["card_last4"] == "719"

    mock_read_excel.assert_called_once()


def test_operation_datetime():
    value = datetime(2021, 12, 31, 16, 44, 0)
    assert operation_datetime(value) is value

    assert operation_datetime("31.12.2021 16:44:00") == datetime(2021, 12, 31, 16, 44, 0)
