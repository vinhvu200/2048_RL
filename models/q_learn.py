from models.estimator import Estimator
from models.enum.direction import Direction
import numpy as np


class Q_Learn():

    def __init__(self, game, episodes, discount, epsilon):
        self.game = game
        self.episodes = episodes
        self.discount = discount
        self.epsilon = epsilon
        self.estimator = Estimator(self.game.action_space,
                                   self.game.get_state())
        self.direction_dict = [Direction.UP,
                               Direction.DOWN,
                               Direction.LEFT,
                               Direction.RIGHT]

    def epsilon_greedy_policy(self, state):

        probs = np.ones(len(state)) * self.epsilon / self.game.action_space
        q_vals = self.estimator.predict(state)
        best_action = np.argmax(q_vals)
        probs[best_action] += (1.0 - self.epsilon)
        return probs

        # A = np.ones(nA, dtype=float) * epsilon / nA
        # q_values = estimator.predict(observation)
        # best_action = np.argmax(q_values)
        # A[best_action] += (1.0 - epsilon)
        # return A

    def learn(self):

        for e in self.episodes():

            state = self.game.get_state()

            for t in xrange(1):

                probs = self.epsilon_greedy_policy(state)

                index = np.random.choice(np.arange(len(state)),
                                          p=probs)
                action = self.direction_dict[index]

                new_state, done = self.game.move(action)

                if done:
                    self.game.replay()
                    self.game.update()
                    break
