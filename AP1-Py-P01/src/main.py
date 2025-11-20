import curses

import pyfiglet
import time
import os
import game_setting
from presentation.render2d.render import Render2d
from presentation.render2d.img_output import screen
from presentation.input import GameInput


class Game:
    def show_title(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for text, color, font in game_setting.GAME_TITLE:
            self.print_color_title(text, color, font)

    def print_color_title(self, text: str, color="red", font="big", delay=0.6):
        if color in game_setting.COLORS and (font == "big" or font == "small"):
            text_art = pyfiglet.figlet_format(text, font=font)
            print(game_setting.COLORS[color] + text_art + game_setting.COLORS['reset'])
            time.sleep(delay)

    def start(self):

        # self.show_title()
        screen.start()

        # render2d = Render2d()
        # render2d.start()


if __name__ == '__main__':
    game = Game()
    game.start()

    game_input = GameInput()
    game_input.wait_for_enter()
    # curses.wrapper(game_input.start)
