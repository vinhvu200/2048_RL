from models.estimator import Estimator
from models.enum.direction import Direction
from sklearn.kernel_approximation import RBFSampler

import matplotlib.pyplot as plt
import numpy as np
import random
import time
import sklearn.pipeline
import sklearn.preprocessing

class Q_Learn():

    def __init__(self, game, episodes, discount, epsilon):

        self.game = game
        self.episodes = episodes
        self.discount = discount
        self.epsilon = epsilon
        self.featurizer = sklearn.pipeline.FeatureUnion([
        ("rbf1", RBFSampler(gamma=5.0, n_components=100)),
        ("rbf2", RBFSampler(gamma=2.0, n_components=100)),
        ("rbf3", RBFSampler(gamma=1.0, n_components=100)),
        ("rbf4", RBFSampler(gamma=0.5, n_components=100))
        ])
        self.scaler = sklearn.preprocessing.StandardScaler()
        self.estimator = None
        #self.estimator.load_data()
        self.direction_dict = [Direction.UP,
                               Direction.DOWN,
                               Direction.LEFT,
                               Direction.RIGHT]

    def alternate(self):

        self.episodes = 10
        count = 0
        points = []
        while True:

            self.random_play(2)

            points = self.learn(points)
            count += 1
            print('Round Finished : {}\n'.format(count))
            self.graph(points)

    def calc_running_avg(self, n1, n2, total):
        return (n1 + n2) / total

    def compare_states(self, s1, s2):
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                return False
        return True

    def epsilon_greedy_policy(self, state):

        probs = np.ones(self.game.action_space, dtype=float) * self.epsilon / self.game.action_space
        f_state = self.featurize_state(state)
        q_vals = self.estimator.predict(f_state)
        best_action = np.argmax(q_vals)
        probs[best_action] += (1.0 - self.epsilon)

        return probs

    def featurize_state(self, state):
        scaled = self.scaler.transform([state])
        featurized = self.featurizer.transform(scaled)
        return featurized[0]

    def fit_scaler_featurizer(self):

        ep = 5
        states = []
        for i in range(ep):

            state = self.game.state
            while True:

                states.append(state)
                m = random.randint(0, 3)
                if m == 0:
                    next_state, reward, done, _ = self.game.move(Direction.UP)
                elif m == 1:
                    next_state, reward, done, _ = self.game.move(Direction.DOWN)
                elif m == 2:
                    next_state, reward, done, _ = self.game.move(Direction.LEFT)
                else:
                    next_state, reward, done, _ = self.game.move(Direction.RIGHT)

                if done is True:
                    self.game.replay()
                    self.game.update()
                    time.sleep(1)
                    break

        obs_examples = np.array(states)
        self.scaler.fit(obs_examples)
        self.featurizer.fit(self.scaler.transform(obs_examples))
        self.estimator = Estimator(self.game.action_space,
                                   self.featurize_state(self.game.state))
        print('Estimator Built')

    def graph(self, y):
        x = [(i+1) for i in range(len(y))]
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel='Episodes', ylabel='Score',
               title='Episodes vs Score')
        ax.grid()
        fig.savefig('graph/results.png')

    def learn(self, points):

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

                if last_count > 5:
                    action_index = random.randint(0, self.game.action_space - 1)
                    action = self.direction_dict[action_index]
                    next_state, reward, done, skip = self.game.move(action)
                    random_count += 1

                if done is True or skip is True:

                    print('Learn Score : {}'.format(self.game.get_score()))
                    #print('Average : {}'.format(self.calc_running_avg(curr_sum, self.game.get_score(), e+1)))
                    print('Random Moves : {}'.format(random_count))

                    if skip is False:
                        print('Saving data')
                        self.estimator.save_data()
                        #print('Episodes complete : {}\nSteps : {}\n'.format(e + 1, t))
                    else:
                        #self.estimator.load_data()
                        pass

                    points.append(self.game.get_score())
                    #curr_sum += self.game.get_score()
                    self.game.replay()
                    time.sleep(1)
                    self.game.update()
                    self.game.highest = self.game.highest_tile()
                    print('-----------')
                    break

                # TD Update
                f_next_state = self.featurize_state(next_state)
                f_state = self.featurize_state(state)
                td_target = reward + self.discount * np.amax(self.estimator.predict(f_next_state))
                self.estimator.update(f_state, action_index, td_target)
                # td_target = reward + self.discount * np.amax(self.estimator.predict(next_state))
                # self.estimator.update(state, action_index, td_target)

                last_state = state
                state = next_state

        return points

    def random_play(self, amount):
        reward = 0
        count = 0
        done = False

        while count < amount:

            state = self.game.state
            while True:

                action_index = random.randint(1, 4)

                if action_index is 1:
                    next_state, reward, done, skip = self.game.move(Direction.RIGHT)
                if action_index is 2:
                    next_state, reward, done, skip = self.game.move(Direction.LEFT)
                if action_index is 3:
                    next_state, reward, done, skip = self.game.move(Direction.DOWN)
                if action_index is 4:
                    next_state, reward, done, skip = self.game.move(Direction.UP)

                # TD Update
                f_state = self.featurize_state(state)
                f_next_state = self.featurize_state(next_state)

                td_target = reward + self.discount * np.amax(self.estimator.predict(f_next_state))
                self.estimator.update(f_state, action_index-1, td_target)

                # td_target = reward + self.discount * np.amax(self.estimator.predict(next_state))
                # self.estimator.update(state, action_index-1, td_target)

                if done is True:
                    print('Random Score : {}\n'.format(self.game.get_score()))
                    self.game.replay()
                    time.sleep(1)
                    self.game.update()
                    self.game.highest = self.game.highest_tile()
                    print('-----------')
                    break

                state = next_state

            count += 1