from dataclasses import dataclass


@dataclass(frozen=True)
class ItemRender:
    symbol: str
    color: str


ITEMS = {
    "treasure": ItemRender("$", "yellow"),  # gold
    "food": ItemRender("%", "magenta"),
    "potion": ItemRender("!", "blue"),
    "scroll": ItemRender("?", "white"),
    "sword": ItemRender(")", "yellow"),
    "key": ItemRender("~", "cyan"),
}

