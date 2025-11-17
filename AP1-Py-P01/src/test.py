from domain.classgame import Game

if __name__ == "__main__":
    game = Game()
    game.new_game("Victor")

    # тестовый вывод
    for row in game.level.map.tiles:
        print("".join(
            "." if tile.walkable else "#" for tile in row
        ))