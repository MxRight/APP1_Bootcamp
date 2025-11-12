from dataclasses import dataclass

@dataclass()
class Room:
    number = None  # порядок комнаты от 1 до 9, 1 ая стартовая, 9ая с лестницей вниз (если не 21 уровень)
    x1: int
    y1: int
    x2: int
    y2: int

    def center(self):
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def intersects(self, other: "Room") -> bool:
        """
        Проверяем пересечение комнат
        :param other:
        :return:
        """
        return (
            self.x1 <= other.x2 and self.x2 >= other.x1
            and self.y1 <= other.y2 and self.y2 >= other.y1
        )