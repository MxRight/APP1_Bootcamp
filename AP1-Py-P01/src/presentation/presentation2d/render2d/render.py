import curses
from .tiles import TILES
from .entities.enemies import ENEMIES
from .entities.items import ITEMS
from .entities.player import PLAYER
from .colors import COLORS
from application.constants import PLAYER_CODE


class Render2d:
    """Класс отрисовки текущего WorldView на экране curses (без мерцания)."""

    def init_colors(self, stdscr):
        curses.start_color()
        for i, (_, (fg, bg)) in enumerate(COLORS.items(), start=1):
            curses.init_pair(i, fg, bg)

    def color_id(self, color_name):
        """Вернуть id цветовой пары по имени (0 если нет)."""
        names = list(COLORS.keys())
        try:
            return names.index(color_name) + 1
        except ValueError:
            return 0

    def draw_world(self, stdscr, world_view):
        """Рисует состояние мира во внутреннем буфере и показывает его за один кадр."""

        height = len(world_view.tiles)
        width = len(world_view.tiles[0]) if height else 0

        pad_h = height + 5
        pad_w = width + 10
        buffer = curses.newpad(pad_h, pad_w)

        for y, row in enumerate(world_view.tiles):
            for x, tile in enumerate(row):
                try:
                    tile_render = TILES[tile.kind]
                    symbol = tile_render.symbol
                    color_id = self.color_id(tile_render.color)
                    buffer.addch(y, x, symbol, curses.color_pair(color_id))
                except (KeyError, curses.error):
                    # Если нет такого тайла или вылезли за границы
                    pass

        for ent in world_view.entities:
            try:
                if ent.kind in PLAYER:
                    data = PLAYER[ent.kind]
                elif ent.kind in ENEMIES:
                    data = ENEMIES[ent.kind]
                elif ent.kind in ITEMS:
                    data = ITEMS[ent.kind]
                else:
                    data = None

                if data:
                    symbol = data.symbol
                    color_id = self.color_id(data.color)
                else:
                    symbol, color_id = "?", 0

                ch = symbol[0] if isinstance(symbol, str) else str(symbol)[0]
                buffer.addch(ent.y, ent.x, ch, curses.color_pair(color_id))
            except curses.error:
                pass  # безопасно игнорируем выход за границы

        hud = world_view.hud
        hud_y = height + 1
        hud_line = f"HP:{hud.hp:3}  Lvl:{hud.level:2}  Treasure:{hud.treasure:3}"
        buffer.addstr(hud_y, 0, hud_line, curses.A_BOLD)

        if world_view.message:
            msg_y = hud_y + 1
            buffer.addstr(msg_y, 0, world_view.message[:width - 1])

        max_y, max_x = curses.LINES - 1, curses.COLS - 1
        buffer.refresh(0, 0, 0, 0, min(max_y, pad_h - 1), min(max_x, pad_w - 1))
