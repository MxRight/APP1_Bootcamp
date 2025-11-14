from dataclasses import dataclass


@dataclass(frozen=True)
class EnemyView:
    symbol: str
    color: str


ENEMIES = {
    "zombie ": EnemyView("z", "green"),
    "vampire": EnemyView("v", "red"),
    "ghost": EnemyView("g", "white"),
    'ogre': EnemyView("o", "yellow"),
    'snake': EnemyView("s", "white"),
    'mimic': EnemyView("m", "white")
}
