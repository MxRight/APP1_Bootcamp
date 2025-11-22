import curses
from .render2d.render import Render2d
from .controller2d.controller2d import Controller2d


class GameUI:
    """Presentation‑слой: управляет отрисовкой и вводом с помощью curses"""

    def __init__(self, world):
        self.world = world
        self.renderer = Render2d()
        self.controller = Controller2d()

    def run(self):
        """Запускает curses‑сессию и главный игровой цикл"""
        curses.wrapper(self.loop)

    def loop(self, stdscr):
        curses.curs_set(0)
        self.renderer.init_colors(stdscr)
        stdscr.nodelay(False)
        stdscr.keypad(True)

        while self.world.running:
            world_view = self.world.to_view()
            self.renderer.draw_world(stdscr, world_view)
            command = self.controller.handle_input(stdscr)
            if command:
                self.world.handle_command(command)
            if command == "quit":
                break

        stdscr.clear()
        stdscr.addstr(0, 0, "Вы покинули подземелье. До новых встреч, герой!")
        stdscr.refresh()
        stdscr.getch()
