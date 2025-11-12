from dataclasses import dataclass

@dataclass
class Tile:
    walkable: bool # Можно ли пройти по этой клетке
    transparent: bool # Можно ли видеть сквозь эту клетку
    kind: str # тип клетки