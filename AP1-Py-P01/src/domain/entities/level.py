import random
from .room import Room
from .game_map import Tile, GameMap
from application.constants import FLOOR_TILE_CODE, PASSAGE_TILE_CODE
from ..game_balance import BASE_ENEMIES, BASE_ITEMS
from .enemy import Enemy
from .item import Item
import datetime


class Level:
    MAX_LEVEL = 21
    QUANTITY_OF_ROOMS = 9

    def __init__(self, width: int, height: int, number: int):
        """Создаёт уровень с заданными размерами и номером."""
        self.number = number
        self.map = GameMap(width, height)
        self.rooms: list[Room] = []
        self.entities = []  # враги, предметы, игрок и т. д.

    def gen_level(self,
                  min_width, max_width,
                  min_height, max_height):
        """Создаёт ровно QUANTITY_OF_ROOMS комнат.
        Размеры зависят от заданных диапазонов и уровня."""
        target_rooms = self.QUANTITY_OF_ROOMS
        attempts = 0
        max_attempts = 300

        # коэффициент "глубины" уровня: чем глубже тем крупнее помещения
        scale = 1.0 + (self.number - 1) * 0.05
        scale = min(scale, 1.5)  # ограничим рост, чтобы не вышло за границы карты

        while len(self.rooms) < target_rooms and attempts < max_attempts:
            attempts += 1

            # отдельные диапазоны ширины и высоты + масштабирование
            w = int(random.randint(min_width, max_width) * scale)
            h = int(random.randint(min_height, max_height) * scale)

            # чтобы не выйти за пределы карты:
            if w >= self.map.width - 4 or h >= self.map.height - 4:
                # комната получилась слишком большой, пересчитаем заново
                continue

            x = random.randint(1, self.map.width - w - 2)
            y = random.randint(1, self.map.height - h - 2)

            new_room = Room(
                number=len(self.rooms) + 1,
                x1=x, y1=y,
                x2=x + w, y2=y + h
            )

            # избегаем пересечений
            if any(new_room.intersects(other) for other in self.rooms):
                continue

            self.carve_room(new_room)

            if self.rooms:
                self.connect_rooms(self.rooms[-1], new_room)

            self.rooms.append(new_room)

        # если попытки исчерпаны, а комнат меньше — просто сообщим
        # if len(self.rooms) < target_rooms:
        #   print(f"[WARNING] Created only {len(self.rooms)} rooms out of {target_rooms}")

    def carve_room(self, room: Room):
        """Вырезает помещение на карте (пол)."""
        for y in range(room.y1 + 1, room.y2):
            for x in range(room.x1 + 1, room.x2):
                self.map.tiles[y][x] = Tile(True, True, FLOOR_TILE_CODE)

    def carve_h_tunnel(self, x1: int, x2: int, y: int):
        """Горизонтальный туннель"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map.tiles[y][x] = Tile(True, True, PASSAGE_TILE_CODE)

    def carve_v_tunnel(self, y1: int, y2: int, x: int):
        """Вертикальный туннель"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map.tiles[y][x] = Tile(True, True, PASSAGE_TILE_CODE)

    def connect_rooms(self, room_a: Room, room_b: Room):
        """Соединяет центры двух комнат случайным порядком коридоров."""
        ax, ay = room_a.center()
        bx, by = room_b.center()

        if random.random() < 0.5:
            self.carve_h_tunnel(ax, bx, ay)
            self.carve_v_tunnel(ay, by, bx)
        else:
            self.carve_v_tunnel(ay, by, ax)
            self.carve_h_tunnel(ax, bx, by)

    def random_free_in_room(self, room):
        """Находит случайную свободную клетку в пределах комнаты."""
        while True:
            x = random.randint(room.x1 + 1, room.x2 - 2)
            y = random.randint(room.y1 + 1, room.y2 - 2)
            # Если клетка проходимая и пустая
            if self.map.tiles[y][x].kind == "floor" and not any(
                    e.x == x and e.y == y for e in self.entities
            ):
                return x, y

    def populate_rooms(self, level_num: int):
        """Распределяет монстров и предметы по комнатам (первая комната пустая)."""
        if not self.rooms or len(self.rooms) < 2:
            return

        # первая комната (игрок) остаётся пустой
        rooms_to_fill = self.rooms[1:]
        self.entities = []

        # коэффициенты сложности
        enemy_factor = 1 + (level_num - 1) * 0.3
        item_factor = max(0.5, 1.3 - level_num * 0.1)

        # фильтруем доступных врагов и предметы по уровню
        available_enemies = [
            (k, v) for k, v in BASE_ENEMIES.items()
            if v["min_level"] <= level_num
        ]
        available_items = [
            (k, v) for k, v in BASE_ITEMS.items()
            if v["min_level"] <= level_num
        ]

        for room in rooms_to_fill:
            density = random.uniform(0.5, 1.5)

            num_enemies = max(0, int(random.randint(0, 2) + enemy_factor * density))
            if available_enemies and num_enemies:
                names, weights = zip(*[(k, data["chance"]) for k, data in available_enemies])
                for _ in range(num_enemies):
                    enemy_key = random.choices(names, weights=weights, k=1)[0]
                    enemy_data = BASE_ENEMIES[enemy_key]
                    enemy_class = enemy_data["class"]
                    x, y = self.random_free_in_room(room)
                    enemy = enemy_class(x, y)
                    enemy.create()
                    self.entities.append(enemy)

            num_items = max(0, int(random.randint(0, 1) + item_factor * random.random()))
            if available_items and num_items:
                # создаём списки для выбора по весам
                classes, weights = zip(*[(cls, data["chance"]) for cls, data in available_items])

                for _ in range(num_items):
                    item_class = random.choices(classes, weights=weights, k=1)[0]
                    x, y = self.random_free_in_room(room)
                    self.entities.append(item_class(x, y))
