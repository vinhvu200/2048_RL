from models.estimator import Estimator
from models.enum.direction import Direction


import numpy as np
import random
import time

class Q_Learn():

    def __init__(self, game, episodes, discount, epsilon):
        self.game = game
        self.episodes = episodes
        self.discount = discount
        self.epsilon = epsilon
        self.estimator = Estimator(self.game.action_space,
                                   self.game.state)
        #self.estimator.load_data()
        self.direction_dict = [Direction.UP,
                               Direction.DOWN,
                               Direction.LEFT,
                               Direction.RIGHT]

    def calc_running_avg(self, n1, n2, total):
        return (n1 + n2) / total

    def compare_states(self, s1, s2):
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                return False
        return True

    def epsilon_greedy_policy(self, state):

        probs = np.ones(self.game.action_space, dtype=float) * self.epsilon / self.game.action_space
        q_vals = self.estimator.predict(state)
        best_action = np.argmax(q_vals)
        probs[best_action] += (1.0 - self.epsilon)

        return probs

    def learn(self):

        last_state = [0 for _ in range(len(self.game.state))]
        last_count = 0
        curr_sum = 0
        for e in range(self.episodes):

            state = self.game.state

            random_count = 0
            for t in range(10000):

                if self.compare_states(state, last_state) is True:
                    last_count += 1
                else:
                    last_count = 0

                # Select and take action
                probs = self.epsilon_greedy_policy(state)
                action_index = np.random.choice(np.arange(self.game.action_space),
                                          p=probs)
                action = self.direction_dict[action_index]
                next_state, reward, done, skip = self.game.move(action)

                if last_count > 10:
                    action_index = random.randint(0, self.game.action_space - 1)
                    action = self.direction_dict[action_index]
                    next_state, reward, done, skip = self.game.move(action)
                    random_count += 1

                # if skip is False and self.compare_states(state, next_state) is True:
                #     action_index = random.randint(0, self.game.action_space - 1)
                #     action = self.direction_dict[action_index]
                #     next_state, reward, done, skip = self.game.move(action)

                if done is True or skip is True:

                    print('Average : {}'.format(self.calc_running_avg(curr_sum, self.game.get_score(), e+1)))
                    print('Random Moves : {}'.format(random_count))

                    if skip is False:
                        print('Saving data')
                        self.estimator.save_data()
                        print('Episodes complete : {}\nSteps : {}\n'.format(e + 1, t))
                    else:
                        #self.estimator.load_data()
                        pass

                    curr_sum += self.game.get_score()
                    self.game.replay()
                    time.sleep(1)
                    self.game.update()
                    break

                # TD Update
                td_target = reward + self.discount * np.amax(self.estimator.predict(next_state))
                self.estimator.update(state, action_index, td_target)

                last_state = state
                state = next_state