# Rogue Remake (under construction - COMING SOON - DECEMBER 1, 2025)
Ремейк классической ролевой игры 1980/83 года

## Архитектура проекта, слои:
- Domain (Бизнес логика)
- View (отрисовка и пользовательский ввод):
    * Render
    * UI
- Datalayer (Хранения истории прошлых игр, таблица рекордов):
    * ->JSON->

 ## Взаимодействие слоев presentation и domain:

### Из presentation в domain

ввод:
например: "move_up", "move_down", "attack", "pickup", "quit"...

### Из domain в presentation

снимок мира class WorldView:
 
```
@dataclass
class EntityView: # сущности с координатами
    x: int
    y: int
    kind: str  # 'player', 'enemy', 'snake', 'item'

@dataclass
class HUDView: # панель состояния игрока
    hp: int
    level: int
    treasure: int 

@dataclass
class WorldView:
    tiles: list[list[str]]  карта местности
    entities: List[EntityView] массив игровых сущностей
    hud: HUDView # панель состояния игрока
    message: str # "Goblin takes 3 damage!"
```
### datalayer