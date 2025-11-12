import pyfiglet
import time
import os
import constants

class Game:
    def show_title(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for text, color, font in constants.GAME_TITLE:
            self.print_color_title(text, color, font)


    def print_color_title(self, text:str, color="red", font="big", delay=0.6):
        if color in constants.COLORS and (font=="big" or font=="small"):
            text_art = pyfiglet.figlet_format(text, font=font)
            print(constants.COLORS[color] + text_art + constants.COLORS['reset'])
            time.sleep(delay)

    def start(self):
        self.show_title()


if __name__ == '__main__':
    game = Game()
    game.start()
