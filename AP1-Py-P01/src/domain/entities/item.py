import random

from .gameobject import GameObject
from application.constants import FOOD_ITEM_CODE, TREASURE_ITEM_CODE, SCROLL_ITEM_CODE, KEY_ITEM_CODE, SWORD_ITEM_CODE, POTION_ITEM_CODE

class Item(GameObject):

    def create(self):
        self.active = True

    def pick_up(self):
        pass


class UseItem(Item):
    def use(self):
        pass


class Treasure(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = TREASURE_ITEM_CODE
        self.cost = self.set_cost()

    def set_cost(self, num = 1):
        return random.randint(1, 10 * num)



class Food(UseItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = FOOD_ITEM_CODE


class Elixir(UseItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = POTION_ITEM_CODE


class Scroll(UseItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = SCROLL_ITEM_CODE


class Weapon(UseItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = Weapon
        self.type = None
        self.strengh = None

    def drop_weapon(self):
        pass

    def generate_weapon(self):
        pass


class Key(UseItem):
    pass
