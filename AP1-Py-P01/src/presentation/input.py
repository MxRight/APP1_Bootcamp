import curses
import sys, termios, tty

class GameInput:
    def __init__(self):
        self.sdtscr = None

    def start(self, sdtscr):
        self.sdtscr = sdtscr
        while True:
            key = self.sdtscr.getch()
            if key in (ord('q'), ord('Q'), 27):  # ESC = 27
                break


    def wait_for_enter(self):
        """Ждать ровно одно нажатие Enter без библиотеки curses для пропуска стартовой картинки"""
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)  # отключаем буферизацию
            while True:
                ch = sys.stdin.read(1)
                if ch == '\r' or ch == '\n':  # Enter
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

