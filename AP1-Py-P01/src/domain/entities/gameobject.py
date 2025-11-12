class GameObject:
    def __init__(self):
        self.x = None
        self.y = None
        self.type = None
        self.active = False  # отображаются и действуют только активные объекты

    def drop_in_room(self, room_id: int):
        pass


class Creature(GameObject):
    def __init__(self):
        super().__init__()
        self.name = None
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
