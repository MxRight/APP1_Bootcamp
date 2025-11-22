from domain.entities.enemy import Enemy
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
        self.level.populate_rooms(self.num_of_level)

    def load_game(self):
        pass

    def save_game(self):
        pass

    def game_over(self):
        pass

    def next_level(self):
        self.num_of_level += 1
        self.level.gen_level(self.num_of_level)
        self.level.populate_rooms(self.num_of_level)

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
                self.update_message("Вы упираетесь в стену.")

            return False
        if tile.kind == DOOR_TILE_CODE:
            if entity is self.player:
                self.update_message("Дверь закрыта.")
            return False


        # Проверка столкновений с другими существами
        for e in [self.player] + self.level.entities:
            if e is entity:
                continue
            if e.x == nx and e.y == ny:
                if isinstance(e, Enemy):
                    if entity is self.player:
                        self.update_message(f"Путь закрыт существом: {e.name}.")
                    return False


        return True

    def try_move_entity(self, entity, dx: int, dy: int):
        """Двигает сущность, если движение возможно."""
        if not self.can_move(entity, dx, dy):
            return

        # вычисляем новые координаты
        nx, ny = entity.x + dx, entity.y + dy
        entity.move(dx, dy)

        # если это игрок — проверяем, есть ли предмет
        if entity is self.player:
            self.check_for_item(nx, ny)

        #self.update_message("")

    def check_for_item(self, x: int, y: int):
        """Проверяет наличие предметов и обрабатывает их подбор."""
        # ищем предмет на этой позиции
        for item in list(self.level.entities):  # делаем копию, т.к. будем удалять
            if getattr(item, "kind", "") and item.x == x and item.y == y:
                # если это сокровище
                if item.kind == "treasure":
                    self.pickup_treasure(item)
                    break
                # если это еда, свиток и т.п. — теоретически другие варианты
                else:
                    self.pickup_generic(item)
                    break

    def pickup_treasure(self, item):
        """Подбор сокровища."""
        cost = item.cost
        self.treasure += cost                # увеличиваем счётчик
        self.level.entities.remove(item)     # убираем предмет из уровня
        self.update_message(f"Вы подняли сокровище, стоимостью {cost} золотых монет!")

    def pickup_generic(self, item):
        """Подбор других предметов (пока просто удаляем)."""
        self.level.entities.remove(item)
        self.update_message(f"Вы подбираете {item.kind.lower()}.")

    def handle_command(self, cmd: str):
        """Обработка команд от пользователя из слоя presentation"""
        if cmd is None:
            return

        self.update_message("")

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
