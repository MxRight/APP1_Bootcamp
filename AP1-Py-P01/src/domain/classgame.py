from domain.entities.player import Player
from domain.entities.level import Level
from application.view_models import WorldView, TileView, EntityView, HUDView
from constants import WIDTH, HEIGHT, MIN_ROOM_W_SIZE, MAX_ROOM_W_SIZE, MIN_ROOM_H_SIZE, MAX_ROOM_H_SIZE



class Game:
    def __init__(self):
        self.player = None  # Player()
        self.treasure = 0
        self.num_of_level = None
        self.level = None  # Level()  # так же можно использовать как коэффициент к уровню монстров, сокровищ и вещей.

    def new_game(self, player_name: str):
        self.num_of_level = 1
        self.player = Player()
        self.player.name = player_name
        self.level = Level(WIDTH, HEIGHT, self.num_of_level)
        self.level.gen_level(MIN_ROOM_W_SIZE, MAX_ROOM_W_SIZE, MIN_ROOM_H_SIZE, MAX_ROOM_H_SIZE)
        self.player.start()

    def load_game(self):
        pass

    def save_game(self):
        pass

    def game_over(self):
        pass

    def next_level(self):
        self.num_of_level += 1
        self.level.gen_level(self.num_of_level)

    def victory(self):
        pass

    def build_view(self) -> WorldView:
        tiles = []
        for y, row in enumerate(self.level.map.tiles):
            tiles_row = []
            for x, tile in enumerate(row):
                tiles_row.append(TileView(
                    kind=tile.kind,
                ))
            tiles.append(tiles_row)

        entities = [
            EntityView(e.x, e.y, e.kind)
            for e in [self.player] + self.level.entities
        ]
        hud = HUDView(hp=self.player.hp, level=self.num_of_level, treasure=self.treasure)

        return WorldView(tiles=tiles, entities=entities, hud=hud, message='временное сообщение')
