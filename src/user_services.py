import re


def search_description(operations: list[dict], word: str) -> list[dict]:
    """Ищет транзакции по подстроке в поле description"""
    w = word.strip().lower()
    if not w: return []
    res = []
    for op in operations:
        description = str(op.get("description", "")).lower()
        if w in description:
            res.append(op)
    return res

def format_phone(phone: str) -> str:
    """Приводит телефон к единому виду"""
    digits = re.sub(r'\D', "", phone)
    if not digits: return ""
    if len(digits) == 10:
        return "7" + digits
    if len(digits) == 11:
        if digits[0] == "8":
            return "7" + digits[1:]
        return digits
    return ""

def find_phone(text: str) -> list[str]:
    """Ищет в description номера телефона"""
    if not text: return []
    pattern = re.findall(r"(\+?\d[\d\s\-\(\)]{8,}\d)", text)
    res = []
    for p in pattern:
        phone = format_phone(p)
        if phone:
            res.append(phone)
    return res

def search_phone(operations: list[dict], phone_pattern: str) -> list[dict]:
    """Ищет транзакции, в описании которых встречается телефон, соответствующий phone_pattern"""
    phone = format_phone(phone_pattern)
    if not phone: return []
    res = []
    for op in operations:
        description = str(op.get("description", ""))
        phones = find_phone(description)
        if phone in phones:
            res.append(op)
    return res