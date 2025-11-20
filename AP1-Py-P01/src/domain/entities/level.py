import random
from .room import Room
from .game_map import Tile, GameMap
from application.constants import FLOOR_TILE_CODE, PASSAGE_TILE_CODE
from .player import Player


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
        #if len(self.rooms) < target_rooms:
         #   print(f"[WARNING] Created only {len(self.rooms)} rooms out of {target_rooms}")

        # враги и предметы

        self.drop_enemy()
        self.drop_items()

    # --------------------- вырезание ходов ---------------------

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



    def drop_enemy(self):
        """Пока просто заглушка — сюда добавится логика спауна врагов."""
        # Например:
        # for room in self.rooms[1:]:
        #     x, y = room.center()
        #     self.entities.append(Enemy("goblin", x, y))
        pass

    def drop_items(self):
        """Пока просто заглушка — сюда добавится логика появления предметов."""
        # Аналогично
        pass
