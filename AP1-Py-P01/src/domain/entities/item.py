from gameobject import GameObject

class Item(GameObject):
    def __init__(self):
        super().__init__()
        self.type_of_item = None  # может быть хватит self.type?

    def set_type_of_item(self):
        self.type_of_item = f"{self.__class__.__name__}"

    def create(self, x, y):
        self.set_type_of_item()
        self.x = x
        self.y = y
        self.active = True

    def pick_up(self):
        pass


class UseItem(Item):
    def use(self):
        pass


class Treasure(Item):
    def set_cost(self):
        # random * level
        pass


class Food(UseItem):
    pass


class Elixir(UseItem):
    pass


class Scroll(UseItem):
    pass


class Weapon(UseItem):
    def __init__(self):
        super().__init__()
        self.strengh = None

    def drop_weapon(self):
        pass

    def generate_weapon(self):
        pass


class Key(UseItem):
    pass
