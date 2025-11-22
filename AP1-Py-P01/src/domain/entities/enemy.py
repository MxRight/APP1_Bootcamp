from .gameobject import Creature
from random import choice
from .item import Treasure
from domain.entities.constants import MONSTERSNAMES
from application.constants import *

# необходимо инициилизировать кодовые переенные

class Enemy(Creature):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hostility = None  # враждебность
        self.behaviour = None  # поведение

    def create(self):
        self.give_name()
        self.active = True

    def give_name(self):
        random_name = choice(MONSTERSNAMES)
        self.name = f"{self.__class__.__name__} {random_name}"

    def say_hello(self):
        pass

    def defeat(self):
        self.active = False

        Treasure().create(self.x, self.y)

    def __repr__(self):
        return f'{self.kind} {self.name}'


class Zombie(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = ZOMBIE_ENEMY_CODE


class Vampire(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = VAMPIRE_ENEMY_CODE


class Ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = GHOST_ENEMY_CODE


class Ogre(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = OGRE_ENEMY_CODE


class Serpent(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = SNAKE_ENEMY_CODE


class Mimic(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = MIMIC_ENEMY_CODE
