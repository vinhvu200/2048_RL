import random
import time

from models.enum.direction import Direction
from models.Game import Game
from models.q_learn import Q_Learn
from sklearn.preprocessing import StandardScaler

game = Game()
game.update()


def play():
    while(game.game_over() is False):

        r = random.randint(1, 4)

        if r is 1:
            next_state, _, _, _ = game.move(Direction.RIGHT)
        if r is 2:
            next_state, _, _, _ = game.move(Direction.LEFT)
        if r is 3:
            next_state, _, _, _ = game.move(Direction.DOWN)
        if r is 4:
            next_state, _, _, _ = game.move(Direction.UP)
    #game.replay()

def manual():
    while game.game_over() is False:

        input = raw_input()
        if input == 'w':
            next_state, reward, done, skip = game.move(Direction.UP)
        if input == 'a':
            next_state, reward, done, skip = game.move(Direction.LEFT)
        if input == 's':
            next_state, reward, done, skip = game.move(Direction.DOWN)
        if input == 'd':
            next_state, reward, done, skip = game.move(Direction.RIGHT)

        q.featurize_state(next_state)

#manual()

episodes = 1000
discount = 0.9
epsilon = 0.0

q = Q_Learn(game, episodes, discount, epsilon)
q.fit_scaler_featurizer()
q.alternate()

# q.random_play(10)
# q.learn()