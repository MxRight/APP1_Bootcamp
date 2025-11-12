from room import Room
from game_map import Tile, GameMap


class Level:
    MAX_LEVEL = 21
    QUANTITY_OF_ROOMS = 9

    class Level:
        def __init__(self, width, height, number):
            self.number = number
            self.map = GameMap(width, height)
            self.rooms: list[Room] = []
            self.entities = []

    def carve_room(self, room: Room):
        """Вырезает комнату на карте — заменяет тайлы на 'пол'."""
        for y in range(room.y1 + 1, room.y2):
            for x in range(room.x1 + 1, room.x2):
                self.map.tiles[y][x] = Tile(
                    walkable=True, transparent=True, kind="floor")

    def carve_h_tunnel(self, x1, x2, y):
        pass

    def carve_v_tunnel(self, y1, y2, x):
        pass

    def connect_rooms(self, room_a: Room, room_b: Room):
        pass

    def generate_rooms(self, num_rooms, min_size, max_size):
        pass

    def drop_enemy(self):
        pass

    def drop_items(self):
        pass
