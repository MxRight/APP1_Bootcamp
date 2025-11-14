from dataclasses import dataclass


@dataclass(frozen=True)
class ItemView:
    symbol: str
    color: str


ITEMS = {
    "treasure": ItemView("$", "yellow"),  # gold
    "food": ItemView("%", "magenta"),
    "potion": ItemView("!", "blue"),
    "scroll": ItemView("?", "white"),
    "sword": ItemView(")", "yellow"),
    "key": ItemView("~", "cyan"),
}

