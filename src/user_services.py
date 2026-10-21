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
