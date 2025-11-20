import curses
from .tiles import TILES
from .entities.enemies import ENEMIES
from .entities.items import ITEMS
from .entities.player import PLAYER
from .colors import COLORS
from application.constants import PLAYER_CODE


class Render2d:
    """Представление (presentation): рисует состояние мира в curses."""

    def __init__(self):
        self.stdscr = None

    def run(self, world_view):
        """Главная точка входа для отрисовки WorldView"""
        curses.wrapper(self._main, world_view)

    def _main(self, stdscr, world_view):
        """Оборачивается curses.wrapper, получает stdscr от curses"""
        self.stdscr = stdscr
        curses.curs_set(0)
        self.init_colors()
        self.draw_world(world_view)
        stdscr.refresh()
        stdscr.getch()  # ждать нажатия (например, Enter или любую клавишу)

    def init_colors(self):
        curses.start_color()
        for i, (_, (fg, bg)) in enumerate(COLORS.items(), start=1):
            curses.init_pair(i, fg, bg)

    def color_id(self, color_name):
        """Построить id цветовой пары по имени"""
        names = list(COLORS.keys())
        try:
            return names.index(color_name) + 1
        except ValueError:
            return 0

    def draw_world(self, world_view):
        """Рисует весь снимок мира на экране"""
        stdscr = self.stdscr
        stdscr.clear()

        for y, row in enumerate(world_view.tiles):
            for x, tile in enumerate(row):
                tile_render = TILES[tile.kind]  # объект TileRender
                symbol = tile_render.symbol  # извлекаем строку
                color_id = self.color_id(tile_render.color)  # берём имя цвета
                try:
                    stdscr.addch(y, x, symbol, curses.color_pair(color_id))
                except curses.error:
                    pass  # не страшно, если вылезло за границы

        for ent in world_view.entities:
            if ent.kind in PLAYER:
                data = PLAYER[ent.kind]  # PlayerRender("@", "yellow")
                symbol = data.symbol
                color_id = self.color_id(data.color)

            elif ent.kind in ENEMIES:
                data = ENEMIES[ent.kind]  # EnemyRender(...)
                symbol = data.symbol
                color_id = self.color_id(data.color)

            elif ent.kind in ITEMS:
                data = ITEMS[ent.kind]  # ItemRender(...)
                symbol = data.symbol
                color_id = self.color_id(data.color)

            else:
                symbol, color_id = "?", 0

            try:
                stdscr.addch(ent.y, ent.x, symbol, curses.color_pair(color_id))
            except curses.error:
                pass  # защита от выхода за границы экрана

            # гарантируем, что символ — один знак
            ch = symbol[0] if isinstance(symbol, str) else str(symbol)[0]

            try:
                if color_id is None:
                    color_id = 0
                stdscr.addch(ent.y, ent.x, ch, curses.color_pair(color_id))
            except curses.error:
                pass

        hud = world_view.hud
        hud_y = len(world_view.tiles) + 1
        stdscr.addstr(hud_y, 0,
                      f"HP: {hud.hp}  Lvl: {hud.level}  Treasure: {hud.treasure}",
                      curses.A_BOLD)

        if world_view.message:
            stdscr.addstr(hud_y + 1, 0, world_view.message)

        stdscr.refresh()
