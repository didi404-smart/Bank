import json
from pathlib import Path


def load_user_settings(path: str) -> dict:
    """Загружает пользовательские настройки из JSON-файла."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
