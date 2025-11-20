from .gameobject import Creature
from .backpack import Backpack
from application.constants import PLAYER_CODE

class Player(Creature):
    STARTHP = 100
    MAXSTARTHP = 100
    STARTDEXTERITY = 8
    STARTSTRENGTH = 9

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.max_health = None
        self.weapon = None
        self.backpack = Backpack()

    def start(self):
        self.health = self.STARTHP
        self.max_health = self.MAXSTARTHP
        self.dexterity = self.STARTDEXTERITY
        self.strength = self.STARTSTRENGTH
        self.set_kind(PLAYER_CODE)


    def dead(self):
        pass