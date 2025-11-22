from domain.entities.player import Player
from domain.entities.level import Level
from application.view_models import WorldView, TileView, EntityView, HUDView
from game_setting import WIDTH, HEIGHT, MIN_ROOM_W_SIZE, MAX_ROOM_W_SIZE, MIN_ROOM_H_SIZE, MAX_ROOM_H_SIZE


class Game:
    def __init__(self):
        self.player = None  # Player()
        self.treasure = 0
        self.num_of_level = None
        self.level = None  # Level()  # так же можно использовать как коэффициент к уровню монстров, сокровищ и вещей.
        self.running = True
        self.message = ""

    def new_game(self, player_name: str):
        self.num_of_level = 1
        self.level = Level(WIDTH, HEIGHT, self.num_of_level)
        self.level.gen_level(MIN_ROOM_W_SIZE, MAX_ROOM_W_SIZE, MIN_ROOM_H_SIZE, MAX_ROOM_H_SIZE)
        x, y = self.level.rooms[0].center()
        self.player = Player(player_name, x, y)
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

    def update_message(self, text):
        self.message = text

    def handle_command(self, cmd: str):
        """Обработка команд от пользователя из слоя presentation"""
        if cmd is None:
            return

        if cmd == "quit":
            self.running = False
            self.update_message("Игра завершена.")
            return

        # движение
        if cmd == "move_up":  # вынести в application, импорировать переменные сюда и в слой presentation2d
            self.player.move(0, -1)
        elif cmd == "move_down":
            self.player.move(0, 1)
        elif cmd == "move_left":
            self.player.move(-1, 0)
        elif cmd == "move_right":
            self.player.move(1, 0)

    def to_view(self) -> WorldView:
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
        hud = HUDView(hp=self.player.health, level=self.num_of_level, treasure=self.treasure)

        return WorldView(tiles=tiles, entities=entities, hud=hud, message='временное сообщение')
