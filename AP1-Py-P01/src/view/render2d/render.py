import curses

class Render2d:
    def __init__(self):
        pass

    def test_output(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Привет, подземелье! Нажми любую клавишу, чтобы выйти.")
        stdscr.refresh()
        stdscr.getch()  # ждать нажатия

    def start(self):
        curses.wrapper(self.test_output)



