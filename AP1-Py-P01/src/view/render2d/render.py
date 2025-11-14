import curses
from .tiles import TILES
from .entities.enemies import ENEMIES
from .entities.items import ITEMS
from .entities.player import PLAYER
from .colors import COLORS


class Render2d:
    def __init__(self):
        self.init_colors()
        self.stdscr = None

    def test_output(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Привет, подземелье! Нажми любую клавишу, чтобы выйти.")
        self.stdscr.refresh()
        self.stdscr.getch()  # ждать нажатия

    def init_colors(self):
        curses.start_color()
        for i, (name, (fg, bg)) in enumerate(COLORS.items(), start=1):
            curses.init_pair(i, fg, bg)

    def draw_tile(self, tile_name, x, y):
        tile = TILES[tile_name]
        color_id = self.color_id(tile.color)
        self.stdscr.addstr(y, x, tile.symbol, curses.color_pair(color_id))

    def draw_enemy(self, enemy_name, x, y):
        enemy = ENEMIES[enemy_name]
        color_id = self.color_id(enemy.color)
        self.stdscr.addstr(y, x, enemy.symbol, curses.color_pair(color_id))

    def draw_item(self, item_name, x, y):
        item = ITEMS[item_name]
        color_id = self.color_id(item.color)
        self.stdscr.addstr(y, x, item.symbol, curses.color_pair(color_id))

    def draw_hero(self, player_name, x, y):
        player = PLAYER[player_name]
        color_id = self.color_id(player.color)
        self.stdscr.addstr(y, x, player.symbol, curses.color_pair(color_id))

    def color_id(self, color_name):
        names = list(COLORS.keys())
        return names.index(color_name) + 1

    def start(self):
        curses.wrapper(self.test_output)
