from gameobject import Creature
from random import choice
from item import Treasure
from domain.entities.constants import MONSTERSNAMES

class Enemy(Creature):


    def __init__(self):
        super().__init__()
        self.hostility = None  # враждебность
        self.behaviour = None  # поведение

    def create(self, room_id):
        self.give_name()
        self.drop_in_room(room_id)
        self.active = True

    def give_name(self):
        random_name = choice(MONSTERSNAMES)
        self.name = f"{self.__class__.__name__} {random_name}"

    def say_hello(self):
        pass

    def defeat(self):
        self.active = False

        Treasure().create(self.x, self.y)


class Zomby(Enemy):
    pass


class Vampire(Enemy):
    pass


class Ghost(Enemy):
    pass


class Ogre(Enemy):
    pass


class Serpent(Enemy):
    pass
