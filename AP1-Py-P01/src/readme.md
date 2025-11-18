# Rogue Remake (under construction - COMING SOON - DECEMBER 1, 2025)
Ремейк классической ролевой игры 1980/83 года

## Архитектура проекта, слои:
- Domain (Бизнес логика)
- Presentation (отрисовка и пользовательский ввод):
    * Render
    * UI
- Application (содержит классы-посредники между слоями Domain и Presentation):
     * class WorldView
  
- Datalayer (Хранения истории прошлых игр, таблица рекордов):
    * ->JSON->

 ## Взаимодействие между слоями:

### Из presentation в domain

модуль input.py обрабатывает нажатие кнопок и передает в domain в виде строк:
например: "move_up", "move_down", "attack", "pickup", "quit"...

### Из domain в presentation

В слое Application описан класс WorldView экземпляр которого создается в слое domain и передается в слой Presentation.
Экземпляр класса WorldView представляет из себя снимок мира, с расположением в данный момент времени комнат, корридоров и сущностей, а также данные панели игрока и сообщений:
 
```
@dataclass
class TileView:
    # класс на вырост для 3d и т.д.
    kind: str  # 'floor', 'wall', 'door', etc.


@dataclass
class EntityView:  # сущности с координатами
    x: int
    y: int
    kind: str  # 'player', 'enemy', 'snake', 'item'


@dataclass
class HUDView:  # панель состояния игрока
    hp: int
    level: int
    treasure: int


@dataclass
class WorldView:
    tiles: list[list[TileView]]  # двумерный массив с картой местности
    entities: list[EntityView]  # массив игровых сущностей
    hud: HUDView  # панель состояния игрока
    message: str  # "Goblin takes 3 damage!"
```

### datalayer
Слой для хранения истории прошлых игр, таблицы рекордов
В данной версии всё будет хранится в формате JSON/
