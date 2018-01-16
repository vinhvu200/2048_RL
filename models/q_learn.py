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
                                   self.game.state)
        self.direction_dict = [Direction.UP,
                               Direction.DOWN,
                               Direction.LEFT,
                               Direction.RIGHT]

    def epsilon_greedy_policy(self, state):

        probs = np.ones(self.game.action_space, dtype=float) * self.epsilon / self.game.action_space
        q_vals = self.estimator.predict(state)
        best_action = np.argmax(q_vals)
        probs[best_action] += (1.0 - self.epsilon)

        return probs

    def learn(self):

        for e in range(self.episodes):

            state = self.game.state

            for t in range(100):

                # Select and take action
                probs = self.epsilon_greedy_policy(state)
                action_index = np.random.choice(np.arange(self.game.action_space),
                                          p=probs)
                action = self.direction_dict[action_index]
                next_state, reward, done = self.game.move(action)

                # TD Update
                td_target = reward + self.discount * np.amax(self.estimator.predict(next_state))
                self.estimator.update(state, action_index, td_target)

                if done:
                    self.game.replay()
                    self.game.update()
                    break
