from dataclasses import dataclass


@dataclass(frozen=True)
class EnemyRender:
    symbol: str
    color: str


ENEMIES = {
    "zombie ": EnemyRender("z", "green"),
    "vampire": EnemyRender("v", "red"),
    "ghost": EnemyRender("g", "white"),
    'ogre': EnemyRender("o", "yellow"),
    'snake': EnemyRender("s", "white"),
    'mimic': EnemyRender("m", "white")
}
