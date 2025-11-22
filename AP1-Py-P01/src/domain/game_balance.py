from domain.entities.enemy import Zombie, Vampire, Ghost, Ogre, Serpent, Mimic
from domain.entities.item import Treasure, Food, Elixir, Scroll, Weapon

"""Настройки игрового баланса: враги и предметы по уровням сложности."""

## временно все враги доступны с 1 уровня, вероятность появления скоровища увеличена

# ВРАГИ
# min_level — с какого уровня монстр может появляться
# weight — относительная "сила" монстра (для рассчёта HP/урона)
# spawn_rate — базовое количество на уровень (+ коэффициент сложности)
# chance — вероятность появления внутри доступных монстров (для случайного выбора)

BASE_ENEMIES = {
    "Zombie": {
        "class": Zombie,
        "min_level": 1,
        "weight": 1,
        "spawn_rate": 4,
        "chance": 0.4,
    },
    "Vampire": {
        "class": Vampire,
        "min_level": 1,
        "weight": 2,
        "spawn_rate": 3,
        "chance": 0.25,
    },
    "Ghost": {
        "class": Ghost,
        "min_level": 1,
        "weight": 3,
        "spawn_rate": 2,
        "chance": 0.15,
    },
    "Ogre": {
        "class": Ogre,
        "min_level": 1,
        "weight": 4,
        "spawn_rate": 2,
        "chance": 0.1,
    },
    "Serpent": {
        "class": Serpent,
        "min_level": 1,
        "weight": 5,
        "spawn_rate": 1,
        "chance": 0.07,
    },
    "Mimic": {
        "class": Mimic,
        "min_level": 1,
        "weight": 6,
        "spawn_rate": 1,
        "chance": 0.03,
    },
}

# ПРЕДМЕТЫ
BASE_ITEMS = {
    Food:     {"min_level": 1, "spawn_rate": 4, "chance": 0.35},
    Elixir:   {"min_level": 2, "spawn_rate": 3, "chance": 0.25},
    Scroll:   {"min_level": 3, "spawn_rate": 2, "chance": 0.2},
    Weapon:    {"min_level": 2, "spawn_rate": 1, "chance": 0.15},
    Treasure: {"min_level": 1, "spawn_rate": 5, "chance": 0.45},  # вернуть rate к 1, chance 0.05
}