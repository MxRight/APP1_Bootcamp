import json

def serialize_game(game_state: dict) -> str:
    """Преобразует структуру данных игры в JSON-строку."""
    return json.dumps(game_state)

def deserialize_game(data: str) -> dict:
    """Создаёт структуру данных из JSON-строки."""
    return json.loads(data)