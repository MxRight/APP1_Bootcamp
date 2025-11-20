class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.kind = None
        self.type = None
        self.active = False  # отображаются и действуют только активные объекты

    def set_kind(self, kind):
        self.kind = kind # устанавливаем слово для интерпретации объекта слоем presentation по заданному словарю

    def drop_in_room(self, room_id: int):
        pass


class Creature(GameObject):
    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name
        self.health = None
        self.dexterity = None
        self.strength = None

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def fight(self):
        pass

    def set_hp(self):
        pass
