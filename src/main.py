from pathlib import Path

from src.utils import read_operations

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main() -> None:
    file_path = PROJECT_ROOT / "data" / "operations.xlsx"
    ops = read_operations(str(file_path))

if __name__ == "__main__":
    main()