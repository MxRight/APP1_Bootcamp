import curses
from .render2d.render import Render2d
from .controller2d.controller2d import Controller2d
from .constants import MENU_ITEMS, SUBTITLE, TITLE


class GameUI:
    """Presentation‑слой: управляет отрисовкой и вводом с помощью curses"""

    def __init__(self, world):
        self.world = world
        self.renderer = Render2d()
        self.controller = Controller2d()

    def run(self):
        """Запускает curses‑сессию и главный игровой цикл"""
        curses.wrapper(self.loop)

    def show_intro(self, stdscr):
        """Отображает основное меню с пунктами и обработкой выбора."""

        stdscr.clear()
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()

        title = TITLE
        subtitle = SUBTITLE

        menu_items = MENU_ITEMS
        current_idx = 0
        selected_option = None

        def draw_menu():
            stdscr.clear()
            stdscr.addstr(h // 2 - len(menu_items) - 4,
                          (w - len(title)) // 2, title, curses.A_BOLD)
            stdscr.addstr(h // 2 - len(menu_items) - 2,
                          (w - len(subtitle)) // 2, subtitle)
            for i, item in enumerate(menu_items):
                x = (w - len(item)) // 2
                y = h // 2 - len(menu_items) // 2 + i
                if i == current_idx:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, item)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, item)
            stdscr.refresh()

        draw_menu()

        # цикл переключения и выбора
        while True:
            key = stdscr.get_wch()

            if key in (curses.KEY_UP, "w", "W"):
                current_idx = (current_idx - 1) % len(menu_items)
            elif key in (curses.KEY_DOWN, "s", "S"):
                current_idx = (current_idx + 1) % len(menu_items)
            elif key in ("\n", " ", curses.KEY_ENTER):  # Enter или Пробел
                selected_option = menu_items[current_idx]
                break
            elif key in ("q", "Q", "\x1b"):  # Esc — выход
                selected_option = "Выход"
                break

            draw_menu()

        stdscr.clear()

        if selected_option == "Новая игра":
            # ввод имени игрока
            self.show_name_input(stdscr)
        elif selected_option == "Загрузить игру":
            stdscr.addstr(h // 2, (w - 20) // 2, "Загрузка сохранения…")
            stdscr.refresh()
            curses.napms(1000)
            # сюда добавляем load_game
        elif selected_option == "Рекордсмены":
            stdscr.addstr(h // 2, (w - 12) // 2, "Пока нет рекордов.")
            stdscr.refresh()
            stdscr.getch()
        elif selected_option == "Выход":
            self.world.running = False

    def show_name_input(self, stdscr):
        """Диалог ввода имени героя (с поддержкой кириллицы)."""
        stdscr.clear()
        curses.curs_set(1)
        h, w = stdscr.getmaxyx()

        stdscr.addstr(h // 2 - 2, (w - 26) // 2, "Введите имя вашего героя:")
        stdscr.refresh()

        hero_name = ""
        name_y = h // 2
        name_x = (w - 20) // 2
        stdscr.move(name_y, name_x)

        while True:
            key = stdscr.get_wch()
            if key in ("\n", "\r", curses.KEY_ENTER):
                hero_name = hero_name.strip()
                if hero_name:
                    break
            elif key in ("\b", "\x7f", curses.KEY_BACKSPACE):
                if hero_name:
                    hero_name = hero_name[:-1]
                    stdscr.addstr(name_y, name_x, " " * 20)
                    stdscr.addstr(name_y, name_x, hero_name)
                    stdscr.move(name_y, name_x + len(hero_name))
            elif isinstance(key, str) and len(key) == 1 and len(hero_name) < 18:
                hero_name += key
                stdscr.addstr(name_y, name_x, hero_name)
                stdscr.move(name_y, name_x + len(hero_name))
            elif key in ("q", "Q"):
                hero_name = ""
                break

        curses.curs_set(0)
        stdscr.clear()

        if hero_name:
            self.world.new_game(hero_name)

    def loop(self, stdscr):
        curses.curs_set(0)
        self.renderer.init_colors(stdscr)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        self.show_intro(stdscr)

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
