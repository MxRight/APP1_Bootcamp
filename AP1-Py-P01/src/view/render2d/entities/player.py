from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerView:
    symbol: str
    color: str


PLAYER = {
    "hero": PlayerView("@", "yellow"),
}
