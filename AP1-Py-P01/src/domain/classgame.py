from domain.entities.gameobject import Player
from domain.entities.level import Level


class Game:
    def __init__(self):
        self.player = None # Player()
        self.treasure = 0
        self.num_of_level = None
        self.level = None # Level()  # так же можно использовать как коэффициент к уровню монстров, сокровищ и вещей.

    def new_game(self, player_name: str):
        self.num_of_level = 1
        self.player = Player()
        self.player.name = player_name
        self.level = Level()
        self.level.gen_level(self.num_of_level)
        self.player.start()

    # в методе старт есть функция drop in room
    # как будет происходить обмен данными если room должна храниться в class Level
    # поместить drop in room в класс level или room?

    def load_game(self):
        pass

    def save_game(self):
        pass

    def game_over(self):
        pass

    def next_level(self):
        self.num_of_level+=1
        self.level.gen_level(self.num_of_level)

    def victory(self):
        pass


