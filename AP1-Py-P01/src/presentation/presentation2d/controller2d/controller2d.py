import curses


class Controller2d:
    """Обрабатывает ввод игрока и возвращает команды для domain."""

    def handle_input(self, stdscr):
        key = stdscr.getch()

        # выход
        if key in (ord("q"), 27):  # q или ESC
            return "quit"

        # движение
        elif key in (curses.KEY_UP, ord("w")):
            return "move_up"
        elif key in (curses.KEY_DOWN, ord("s")):
            return "move_down"
        elif key in (curses.KEY_LEFT, ord("a")):
            return "move_left"
        elif key in (curses.KEY_RIGHT, ord("d")):
            return "move_right"

        # использование предметов из рюкзака
        elif key == ord("h"):
            return "use_weapon"
        elif key == ord("j"):
            return "use_food"
        elif key == ord("k"):
            return "use_potion"
        elif key == ord("e"):
            return "use_scroll"

        # ничего не произошло
        else:
            return None
