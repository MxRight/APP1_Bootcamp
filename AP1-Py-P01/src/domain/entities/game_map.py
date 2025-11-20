from .map_tile import Tile
from application.constants import WALL_TILE_CODE

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(False, False, WALL_TILE_CODE) for _ in range(width)] for _ in range(height)] # заполняем всё пространство стенами, позже прорубим комнаты и проходы

    def is_walkable(self, x, y):
        return self.tiles[y][x].walkable