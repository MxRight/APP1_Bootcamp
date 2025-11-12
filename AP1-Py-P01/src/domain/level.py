from room import Room


class Level:
    MAX_LEVEL = 21
    QUANTITY_OF_ROOMS = 9

    def __init__(self):
        self.rooms = [] # массив Rooms???

    def gen_level(self, level: int):
        pass

    def drop_enemy(self):
        pass

    def drop_items(self):
        pass
