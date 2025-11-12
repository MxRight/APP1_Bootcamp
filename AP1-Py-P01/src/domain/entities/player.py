from gameobject import Creature
from backpack import Backpack

class Player(Creature):
    STARTHP = 100
    MAXSTARTHP = 100
    STARTDEXTERITY = 8
    STARTSTRENGTH = 9

    def __init__(self):
        super().__init__()
        self.max_health = None
        self.weapon = None
        self.backpack = Backpack()

    def start(self):  # надо сделать универсальной для стартов уровней
        self.health = self.STARTHP
        self.max_health = self.MAXSTARTHP
        self.dexterity = self.STARTDEXTERITY
        self.strength = self.STARTSTRENGTH
        self.drop_in_room(1)

    def dead(self):
        pass