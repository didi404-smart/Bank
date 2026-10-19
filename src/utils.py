from datetime import datetime

import pandas as pd


def operation_datetime(value) -> datetime:
    """Преобразует значение из столбца «Дата операции» в объект datetime."""
    if isinstance(value, datetime):
        return value
    return datetime.strptime(str(value).strip(), "%d.%m.%Y %H:%M:%S")


def read_operations(path: str) -> list[dict]:
    """Считывает транзакции из Excel-файла и возвращает их в нормализованном виде."""
    df = pd.read_excel(path)
    df = df.dropna(subset=["Дата операции"])
    operations = []
    for num, row in df.iterrows():
        op_dt = operation_datetime(row["Дата операции"])
        card = row.get("Номер карты")
        card_last4 = None
        if pd.notna(card):
            s = str(card).strip()
            if len(s) >= 4:
                card_last4 = s[-4:]
            else:
                card_last4 = s
        operations.append(
            {
                "operation_datetime": op_dt,
                "card_last4": card_last4,
                "status": str(row.get("Статус", "") or "").strip(),
                "amount": float(row.get("Сумма платежа", 0) or 0),
                "currency": str(row.get("Валюта платежа", "") or "").strip(),
                "category": str(row.get("Категория", "") or "").strip(),
                "description": str(row.get("Описание", "") or "").strip(),
            }
        )
    return operations
