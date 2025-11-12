from random import choice


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


class Enemy(Creature):
    MONSTERSNAMES = ["Вася", "Петя"]

    def __init__(self):
        super().__init__()
        self.hostility = None  # враждебность
        self.behaviour = None  # поведение

    def create(self, room_id):
        self.give_name()
        self.drop_in_room(room_id)
        self.active = True

    def give_name(self):
        random_name = choice(self.MONSTERSNAMES)
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


