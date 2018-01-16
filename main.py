import random

from models.enum.direction import Direction
from models.Game import Game
from models.q_learn import Q_Learn

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
    game.replay()

# done = False
# while True:
#     r = random.randint(1, 4)
#
#     if r is 1:
#         next_state, reward, done = game.move(Direction.RIGHT)
#     if r is 2:
#         next_state, reward, done = game.move(Direction.LEFT)
#     if r is 3:
#         next_state, reward, done = game.move(Direction.DOWN)
#     if r is 4:
#         next_state, reward, done = game.move(Direction.UP)
#
#     if done is True:
#         print('here')
#         break

episodes = 200
discount = 0.9
epsilon = 0.05

q = Q_Learn(game, episodes, discount, epsilon)
q.learn()