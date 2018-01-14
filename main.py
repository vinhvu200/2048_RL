import random

from models.enum.direction import Direction
from models.Game import Game

game = Game()
game.update()


def play():
    while(game.game_over() is False):
        r = random.randint(1, 4)

        if r is 1:
            game.move(Direction.RIGHT)
        if r is 2:
            game.move(Direction.LEFT)
        if r is 3:
            game.move(Direction.DOWN)
        if r is 4:
            game.move(Direction.UP)

    game.update()
    print(game.board)

# while True:
#     play()
play()