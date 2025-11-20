from dataclasses import dataclass


@dataclass(frozen=True)
class TileRender:
    symbol: str
    color: str


TILES = {
    "floor": TileRender(".", "white"),
    "wall": TileRender("#", "yellow"),
    "passage": TileRender(".", "white"),
    "door": TileRender("+", "magenta"),
}
