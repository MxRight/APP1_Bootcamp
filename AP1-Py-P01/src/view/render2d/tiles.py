from dataclasses import dataclass


@dataclass(frozen=True)
class TileView:
    symbol: str
    color: str


TILES = {
    "floor": TileView(".", "white"),
    "wall": TileView("#", "yellow"),
    "passage": TileView("=", "yellow"),
    "door": TileView("+", "magenta"),
}
