from domain.entities.player import Player
from domain.entities.level import Level
from application.view_models import WorldView, TileView, EntityView, HUDView
from game_setting import WIDTH, HEIGHT, MIN_ROOM_W_SIZE, MAX_ROOM_W_SIZE, MIN_ROOM_H_SIZE, MAX_ROOM_H_SIZE
from application.constants import WALL_TILE_CODE, DOOR_TILE_CODE


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

    def can_move(self, entity, dx: int, dy: int) -> bool:
        """Проверяет, может ли сущность переместиться на dx, dy."""
        x, y = entity.x, entity.y
        nx, ny = x + dx, y + dy

        map_h = len(self.level.map.tiles)
        map_w = len(self.level.map.tiles[0])
        if not (0 <= nx < map_w and 0 <= ny < map_h):
            if entity is self.player:
                self.update_message("Дальше — пустота.")
            return False

        tile = self.level.map.tiles[ny][nx]
        if tile.kind in (WALL_TILE_CODE,):
            if entity is self.player:
                self.update_message("Ты упираешься в стену.")
            return False
        if tile.kind == DOOR_TILE_CODE:
            if entity is self.player:
                self.update_message("Дверь закрыта.")
            return False

        """
        # Проверка столкновений с другими существами
        for e in [self.player] + self.level.entities:
            if e is entity:
                continue
            if e.x == nx and e.y == ny:
                # можно обработать тип взаимодействия
                if entity is self.player:
                    self.update_message(f"Путь закрыт существом: {e.kind}.")
                return False
        """

        return True

    def try_move_entity(self, entity, dx: int, dy: int):
        """Двигает сущность, если движение возможно."""
        if self.can_move(entity, dx, dy):
            entity.move(dx, dy)
            if entity is self.player:
                self.update_message("")  # очистить старое сообщение
        # иначе player.message уже выставлено в can_move()

    def handle_command(self, cmd: str):
        """Обработка команд от пользователя из слоя presentation"""
        if cmd is None:
            return

        if cmd == "quit":
            self.running = False
            self.update_message("Игра завершена.")
            return

        # движение: вынести "текстовые команды" в application, импорировать переменные сюда и в слой presentation2d
        if cmd == "move_up":
            self.try_move_entity(self.player, 0, -1)
        elif cmd == "move_down":
            self.try_move_entity(self.player, 0, 1)
        elif cmd == "move_left":
            self.try_move_entity(self.player, -1, 0)
        elif cmd == "move_right":
            self.try_move_entity(self.player, 1, 0)

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

        return WorldView(tiles=tiles, entities=entities, hud=hud, message=self.message)
