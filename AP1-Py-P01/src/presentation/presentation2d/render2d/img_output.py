import os
from rich.console import Console
from rich_pixels import Pixels
from .constants import DEFAULT_PATH, DEFAULT_FILENAME


class PrintImg:

    def __init__(self):
        self.stdscr = None
        self.console = Console()
        self.img = None
        self.size = os.get_terminal_size()

    def load_img(self, filename=DEFAULT_FILENAME, path=DEFAULT_PATH):
        # перенести в datalayer?
        try:
            self.img = Pixels.from_image_path(DEFAULT_PATH + DEFAULT_FILENAME,
                                              resize=(self.size.columns, self.size.lines * 2))
        except FileNotFoundError:
            print(f'Ошибка: Файл {filename} не найден!')
            exit(1)

    def start(self):
        self.console.show_cursor(show=False)
        self.load_img()
        self.console.print(self.img)


screen = PrintImg()
