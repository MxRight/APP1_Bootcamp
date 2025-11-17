from dataclasses import dataclass
from typing import Optional

@dataclass
class Room:
    number: Optional[int]  # Порядковый номер комнаты (1–9).
    x1: int
    y1: int
    x2: int
    y2: int

    def center(self) -> tuple[int, int]:
        """Возвращает координаты центра комнаты."""
        cx = (self.x1 + self.x2) // 2
        cy = (self.y1 + self.y2) // 2
        return cx, cy

    def intersects(self, other: "Room") -> bool:
        """Проверяем пересечение комнат"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )