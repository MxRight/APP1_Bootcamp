from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerRender:
    symbol: str
    color: str


PLAYER = {
    "player": PlayerRender("@", "yellow"),
}
