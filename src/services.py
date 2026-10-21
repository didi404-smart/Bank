import re


def search_text(operations: list[dict], query: str) -> dict:
    """Ищет транзакции по подстроке в поле description and category"""
    q = query.strip().lower()
    if not q:
        return {"query": query, "results": []}

    def match(op: dict) -> bool:
        desc = str(op.get("description") or "").lower()
        cat = str(op.get("category") or "").lower()
        return q in desc or q in cat

    return {"query": query, "results": list(filter(match, operations))}


def format_phone(phone: str) -> str:
    """Приводит телефон к единому виду"""
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return ""
    if len(digits) == 10:
        return "7" + digits
    if len(digits) == 11:
        if digits[0] == "8":
            return "7" + digits[1:]
        return digits
    return ""


def find_phone(text: str) -> list[str]:
    """Ищет в тексте номера телефона"""
    if not text:
        return []
    pattern = re.findall(r"(\+?\d[\d\s\-\(\)]{8,}\d)", text)
    res = []
    for p in pattern:
        phone = format_phone(p)
        if phone:
            res.append(phone)
    return res


def search_phone(operations: list[dict], phone_pattern: str) -> dict:
    """Ищет транзакции, в описании которых встречается телефон, соответствующий phone_pattern"""
    phone = format_phone(phone_pattern)
    if not phone:
        return {"phone": phone_pattern, "results": []}

    def match(op: dict) -> bool:
        desc = str(op.get("description") or "")
        return phone in find_phone(desc)

    return {"phone": phone_pattern, "results": list(filter(match, operations))}
