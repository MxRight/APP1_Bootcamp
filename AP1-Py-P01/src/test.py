from domain.classgame import Game
from presentation.render2d.render import Render2d

if __name__ == "__main__":
    game = Game()
    game.new_game("Victor")
    #print(game.level.rooms)
    render2d = Render2d()
    worldview = game.build_view()
    render2d.run(worldview)

