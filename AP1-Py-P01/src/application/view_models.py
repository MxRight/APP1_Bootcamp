#
# классы-посредники между слоями
#
from dataclasses import dataclass


@dataclass
class TileView:
    # класс на вырост для 3d и т.д.
    kind: str  # 'floor', 'wall', 'door', etc.


@dataclass
class EntityView:  # сущности с координатами
    x: int
    y: int
    kind: str  # 'player', 'enemy', 'snake', 'item'


@dataclass
class HUDView:  # панель состояния игрока
    hp: int
    level: int
    treasure: int


@dataclass
class WorldView:
    tiles: list[list[TileView]]  # двумерный массив с картой местности
    entities: list[EntityView]  # массив игровых сущностей
    hud: HUDView  # панель состояния игрока
    message: str  # "Goblin takes 3 damage!"
