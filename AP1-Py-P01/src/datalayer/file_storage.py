from pathlib import Path

def write_file(filename: str, data: str) -> None:
    """Сохраняем строковые данные в файл."""
    path = Path(filename)
    path.write_text(data, encoding='utf-8')

def read_file(filename: str) -> str:
    """Читаем строковые данные из файла."""
    path = Path(filename)
    return path.read_text(encoding='utf-8')