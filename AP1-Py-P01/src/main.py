from domain.classgame import Game
from presentation.presentation2d.gameUI import GameUI
from presentation.presentation2d.render2d.img_output import screen
import time


def main():
    screen.start()
    time.sleep(2)
    game = Game()
    ui = GameUI(game)

    ui.run()


if __name__ == "__main__":
    main()
